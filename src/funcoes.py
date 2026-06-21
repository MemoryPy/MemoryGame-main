# Aqui ficam as funcoes de "regra" do jogo, ou seja, a parte de calculo e
# decisao. Elas nao desenham nada na tela: so recebem valores e devolvem
# respostas. Por serem assim, sao faceis de testar (ver tests/test_logica.py).

import random

from src.config import COMBO_INCREMENTO, COMBO_MAXIMO


def montar_simbolos_do_nivel(simbolos, numero_pares, simbolos_especiais, ativar_especiais):
    """Monta a lista de simbolos (um por par) que vai ser usada no tabuleiro.

    Pega os primeiros 'numero_pares' simbolos normais. Se as cartas
    especiais estiverem ativas e o nivel tiver pares suficientes, troca os
    ultimos simbolos normais pelos especiais (curinga, bonus de tempo e
    embaralha), mantendo o total de pares igual.
    """
    base = list(simbolos[:numero_pares])

    cabe_especiais = numero_pares >= len(simbolos_especiais) + 1
    if ativar_especiais and cabe_especiais:
        quantidade_normais = numero_pares - len(simbolos_especiais)
        base = base[:quantidade_normais] + list(simbolos_especiais)

    return base


def criar_valores_embaralhados(simbolos):
    """Monta as cartas do tabuleiro e embaralha.

    Recebe a lista de letras (uma por par) e devolve uma lista com cada
    letra repetida duas vezes, em ordem aleatoria. E isso que garante que
    cada partida fique diferente.
    """
    valores = list(simbolos) * 2
    random.shuffle(valores)
    return valores


def indice_para_coordenada(indice, colunas):
    """Descobre em que linha e coluna uma carta fica.

    As cartas ficam guardadas numa lista (posicao 0, 1, 2...), mas na tela
    elas formam uma grade. Esta funcao traduz a posicao na lista para o par
    (linha, coluna) correspondente.
    """
    linha = indice // colunas
    coluna = indice % colunas
    return (linha, coluna)


def verificar_par(valor_a, valor_b):
    """Diz se duas cartas formam um par (ou seja, se sao iguais)."""
    return valor_a == valor_b


def calcular_pontos(pontos_atual, pontos_ganhos):
    """Soma os pontos que o jogador acabou de ganhar ao total dele."""
    return pontos_atual + pontos_ganhos


def calcular_bonus_tempo(tempo_restante, pontos_por_segundo):
    """Calcula os pontos extras por terminar a partida com tempo de sobra.

    Cada segundo que sobrou vale alguns pontos. Se nao sobrou tempo, nao ha
    bonus (o 'if' tambem protege contra valores negativos por seguranca).
    """
    if tempo_restante <= 0:
        return 0
    return tempo_restante * pontos_por_segundo


def todos_pares_encontrados(pares_encontrados, numero_pares):
    """Diz se o jogador ja achou todos os pares, ou seja, se venceu."""
    return len(pares_encontrados) >= numero_pares


def eh_novo_recorde(pontuacao, recorde):
    """Diz se a pontuacao desta partida e maior que o recorde salvo."""
    return pontuacao > recorde


def calcular_precisao(tentativas, pares_encontrados):
    """Calcula a porcentagem de tentativas que resultaram em par encontrado.

    Cada tentativa "gasta" e uma jogada de duas cartas; cada par encontrado
    usou exatamente uma dessas tentativas para dar certo. Se o jogador ainda
    nao tentou nenhuma vez, a precisao e 0 (evita dividir por zero).
    """
    if tentativas <= 0:
        return 0.0
    return round((pares_encontrados / tentativas) * 100, 1)


def atualizar_combo(combo_atual, acertou):
    """Atualiza a sequencia de acertos seguidos (combo).

    Um acerto soma 1 ao combo; um erro zera a sequencia, porque o combo so
    vale para acertos consecutivos.
    """
    if acertou:
        return combo_atual + 1
    return 0


def calcular_multiplicador_combo(combo, incremento=COMBO_INCREMENTO, maximo=COMBO_MAXIMO):
    """Calcula o multiplicador de pontos pelo combo atual.

    Cada acerto em sequencia aumenta o multiplicador, mas ele nao passa do
    valor maximo configurado (para o combo nao deixar a pontuacao gigante).
    """
    multiplicador = 1.0 + combo * incremento
    return min(multiplicador, maximo)


def atualizar_estatisticas(estatisticas, venceu, tentativas, tempo_restante):
    """Atualiza as estatisticas pessoais de um nivel apos uma partida.

    Guarda o menor numero de tentativas e o maior tempo restante (melhor
    tempo) entre todas as vitorias, alem do total de partidas jogadas.
    Recebe e devolve um dicionario novo, sem alterar o original.
    """
    novas = dict(estatisticas)
    novas["partidas"] = novas.get("partidas", 0) + 1

    if venceu:
        novas["vitorias"] = novas.get("vitorias", 0) + 1

        menor_tentativas = novas.get("menor_tentativas")
        if menor_tentativas is None or tentativas < menor_tentativas:
            novas["menor_tentativas"] = tentativas

        melhor_tempo = novas.get("melhor_tempo")
        if melhor_tempo is None or tempo_restante > melhor_tempo:
            novas["melhor_tempo"] = tempo_restante

    return novas


def verificar_conquistas(resumo_partida, conquistas_atuais):
    """Verifica quais conquistas o jogador desbloqueou nesta partida.

    Recebe um resumo com os numeros da partida (tentativas, pares, tempo
    restante, nivel, dicas usadas e total de partidas ja jogadas) e o
    conjunto de conquistas que ele ja tinha. Devolve as conquistas NOVAS
    (que ainda nao estavam no conjunto atual).
    """
    desbloqueadas = set()

    if resumo_partida["tentativas"] == resumo_partida["numero_pares"]:
        desbloqueadas.add("perfeito")

    if resumo_partida["tempo_restante"] >= resumo_partida["tempo_limite"] / 2:
        desbloqueadas.add("sobrou_tempo")

    if resumo_partida.get("dicas_usadas", 0) == 0:
        desbloqueadas.add("sem_dica")

    if resumo_partida["nivel"] == "extremo":
        desbloqueadas.add("extremo_concluido")

    if resumo_partida.get("total_partidas", 0) >= 10:
        desbloqueadas.add("veterano")

    # So devolve as conquistas que ainda nao estavam no conjunto atual.
    novas = set()
    for conquista in desbloqueadas:
        if conquista not in conquistas_atuais:
            novas.add(conquista)
    return novas


def qualifica_para_ranking(ranking_nivel, pontos, tamanho_maximo):
    """Diz se uma pontuacao e boa o suficiente para entrar no ranking.

    Entra se ainda ha vagas no ranking (lista menor que o tamanho maximo) ou
    se a pontuacao supera a menor pontuacao que ja esta na lista.
    """
    if len(ranking_nivel) < tamanho_maximo:
        return True

    pior_pontuacao = ranking_nivel[0]["pontos"]
    for item in ranking_nivel:
        if item["pontos"] < pior_pontuacao:
            pior_pontuacao = item["pontos"]

    return pontos > pior_pontuacao


def atualizar_ranking(ranking_nivel, nome, pontos, tamanho_maximo):
    """Inclui um novo nome/pontuacao no ranking e devolve a lista atualizada.

    A lista fica ordenada da maior para a menor pontuacao e e cortada para
    o tamanho maximo (top N), descartando as pontuacoes mais baixas.
    """
    nova_lista = list(ranking_nivel)
    nova_lista.append({"nome": nome, "pontos": pontos})

    # Ordena da maior para a menor pontuacao "na mao": procura repetidas
    # vezes o maior valor que ainda nao foi colocado na lista ordenada.
    ordenada = []
    while nova_lista:
        maior = nova_lista[0]
        for item in nova_lista:
            if item["pontos"] > maior["pontos"]:
                maior = item
        ordenada.append(maior)
        nova_lista.remove(maior)

    return ordenada[:tamanho_maximo]


def completar_par_bonus(valores_ocultos):
    """Escolhe um par ainda oculto para ser completado pela carta curinga.

    Recebe a lista de valores das cartas ainda nao encontradas (sem contar
    a propria curinga) e devolve um valor sorteado entre eles, ou None se
    nao houver nenhum par oculto para completar.
    """
    if not valores_ocultos:
        return None
    return random.choice(valores_ocultos)


def reembaralhar_ocultas(valores_ocultos):
    """Sorteia uma nova ordem para os valores das cartas ainda ocultas.

    Usado pela carta especial "embaralha tudo": pega os valores das cartas
    que ainda nao foram encontradas e devolve eles numa ordem nova, sem
    adicionar nem remover nenhum (so muda a posicao de cada um).
    """
    embaralhados = list(valores_ocultos)
    random.shuffle(embaralhados)
    return embaralhados
