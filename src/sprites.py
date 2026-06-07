import pygame

from src.config import (
    CARTA_OCULTA,
    CARTA_ABERTA,
    CARTA_ENCONTRADA,
    TEXTO_CARTA,
    TEXTO_CLARO,
)


def desenhar_carta(tela, carta, fonte):
    """Desenha uma carta na tela conforme o seu estado atual.

    - Encontrada: fundo verde com o símbolo.
    - Revelada (virada nesta jogada): fundo claro com o símbolo.
    - Oculta: fundo escuro com um "?".
    """
    rect = carta["rect"]

    if carta["encontrada"]:
        cor_fundo = CARTA_ENCONTRADA
        mostrar_simbolo = True
    elif carta["revelada"]:
        cor_fundo = CARTA_ABERTA
        mostrar_simbolo = True
    else:
        cor_fundo = CARTA_OCULTA
        mostrar_simbolo = False

    pygame.draw.rect(tela, cor_fundo, rect, border_radius=12)

    if mostrar_simbolo:
        texto = fonte.render(carta["valor"], True, TEXTO_CARTA)
    else:
        texto = fonte.render("?", True, TEXTO_CLARO)

    posicao_texto = texto.get_rect(center=rect.center)
    tela.blit(texto, posicao_texto)


def desenhar_texto(tela, texto, fonte, cor, centro):
    """Desenha um texto simples centralizado em uma posição."""
    superficie = fonte.render(texto, True, cor)
    retangulo = superficie.get_rect(center=centro)
    tela.blit(superficie, retangulo)
