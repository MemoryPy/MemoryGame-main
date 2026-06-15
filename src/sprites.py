# Aqui ficam as funcoes que desenham as cartas e os textos na tela.
# A parte visual do jogo fica separada da parte de regras (funcoes.py)
# para deixar o codigo mais organizado.

import pygame

from src.config import (
    CARTA_OCULTA,
    CARTA_ABERTA,
    CARTA_ENCONTRADA,
    TEXTO_CARTA,
    TEXTO_CLARO,
)


def desenhar_carta(tela, carta, fonte):
    """Desenha uma carta, mudando a aparencia conforme o estado dela.

    Sao tres situacoes possiveis:
    - ja encontrada: fundo verde e mostra a letra;
    - virada agora nesta jogada: fundo claro e mostra a letra;
    - ainda escondida: fundo escuro e mostra um "?".
    """
    rect = carta["rect"]

    # Escolhe a cor do fundo e se a letra deve aparecer, conforme o estado.
    if carta["encontrada"]:
        cor_fundo = CARTA_ENCONTRADA
        mostrar_simbolo = True
    elif carta["revelada"]:
        cor_fundo = CARTA_ABERTA
        mostrar_simbolo = True
    else:
        cor_fundo = CARTA_OCULTA
        mostrar_simbolo = False

    # Desenha o retangulo da carta com cantos arredondados.
    pygame.draw.rect(tela, cor_fundo, rect, border_radius=12)

    # Escreve a letra (se a carta estiver aberta) ou o "?" (se estiver oculta).
    if mostrar_simbolo:
        texto = fonte.render(carta["valor"], True, TEXTO_CARTA)
    else:
        texto = fonte.render("?", True, TEXTO_CLARO)

    posicao_texto = texto.get_rect(center=rect.center)
    tela.blit(texto, posicao_texto)


def desenhar_texto(tela, texto, fonte, cor, centro):
    """Escreve um texto na tela, centralizado na posicao informada.

    Usada o tempo todo para mostrar placar, titulos e botoes, evitando
    repetir as mesmas linhas em varios lugares.
    """
    superficie = fonte.render(texto, True, cor)
    retangulo = superficie.get_rect(center=centro)
    tela.blit(superficie, retangulo)
