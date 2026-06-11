import random


def criar_valores_embaralhados(simbolos):
    """Monta a lista de cartas (cada símbolo aparece duas vezes) e embaralha.

    Recebe a lista de símbolos disponíveis (um por par) e devolve uma lista
    com o dobro de itens, em ordem aleatória, pronta para preencher a grade.
    """
    valores = list(simbolos) * 2
    random.shuffle(valores)
    return valores


def indice_para_coordenada(indice, colunas):
    """Converte a posição na lista para a coordenada (linha, coluna) da grade."""
    linha = indice // colunas
    coluna = indice % colunas
    return (linha, coluna)


def verificar_par(valor_a, valor_b):
    """Indica se as duas cartas reveladas formam um par igual."""
    return valor_a == valor_b


def calcular_pontos(pontos_atual, pontos_ganhos):
    """Soma os pontos ganhos à pontuação atual."""
    return pontos_atual + pontos_ganhos

def calcular_bonus_tempo(tempo_restante, pontos_por_segundo):
    """Calcula o bônus de pontos pelo tempo que sobrou ao vencer.

    Cada segundo restante vale 'pontos_por_segundo'. Tempo zero (ou
    negativo, por segurança) não gera bônus.
    """
    if tempo_restante <= 0:
        return 0
    return tempo_restante * pontos_por_segundo


def todos_pares_encontrados(pares_encontrados, numero_pares):
    """Verifica se o jogador já encontrou todos os pares do tabuleiro."""
    return len(pares_encontrados) >= numero_pares


def eh_novo_recorde(pontuacao, recorde):
    """Indica se a pontuação atual supera o recorde salvo."""
    return pontuacao > recorde
