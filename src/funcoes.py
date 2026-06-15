# Aqui ficam as funcoes de "regra" do jogo, ou seja, a parte de calculo e
# decisao. Elas nao desenham nada na tela: so recebem valores e devolvem
# respostas. Por serem assim, sao faceis de testar (ver tests/test_logica.py).

import random


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
