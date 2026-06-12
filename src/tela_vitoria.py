import pygame

from src.config import (
    LARGURA_TELA,
    ALTURA_TELA,
    FUNDO,
    BRANCO,
    CINZA,
    CARTA_ENCONTRADA,
    TEXTO_CLARO,
    TEXTO_CARTA,
    TEMPO_LIMITE,
)


# Cores extras usadas só nesta tela
DOURADO = (255, 215, 60)
DOURADO_ESCURO = (200, 160, 0)
AZUL_CARD = (45, 50, 75)
BORDA_CARD = (80, 90, 130)
VERDE_CLARO = (160, 230, 170)
LARANJA = (255, 160, 50)


def _desenhar_texto(tela, texto, fonte, cor, centro):
    """Utilitário interno: renderiza texto centralizado."""
    sup = fonte.render(texto, True, cor)
    ret = sup.get_rect(center=centro)
    tela.blit(sup, ret)


def _desenhar_card(tela, x, y, largura, altura):
    """Desenha um card arredondado com fundo semi-transparente."""
    surf = pygame.Surface((largura, altura), pygame.SRCALPHA)
    pygame.draw.rect(surf, (*AZUL_CARD, 220), (0, 0, largura, altura), border_radius=14)
    pygame.draw.rect(surf, (*BORDA_CARD, 180), (0, 0, largura, altura), width=2, border_radius=14)
    tela.blit(surf, (x, y))


def _desenhar_estrelas(tela, cx, y, n=3):
    """Desenha n estrelas douradas lado a lado, centradas em cx."""
    tamanho = 22
    espaco = 14
    total = n * tamanho + (n - 1) * espaco
    inicio_x = cx - total // 2

    for i in range(n):
        sx = inicio_x + i * (tamanho + espaco) + tamanho // 2
        _desenhar_estrela(tela, sx, y + tamanho // 2, tamanho // 2, DOURADO)


def _desenhar_estrela(tela, cx, cy, raio, cor):
    """Desenha uma estrela de 5 pontas."""
    import math
    pontos = []
    for i in range(10):
        angulo = math.pi / 2 + i * math.pi / 5
        r = raio if i % 2 == 0 else raio * 0.45
        pontos.append((
            cx + r * math.cos(angulo),
            cy - r * math.sin(angulo),
        ))
    pygame.draw.polygon(tela, cor, pontos)
    pygame.draw.polygon(tela, DOURADO_ESCURO, pontos, width=1)


def desenhar_tela_vitoria(tela, estado, recorde, novo_recorde, tempo_gasto):
    # --- Overlay escuro semi-transparente ---
    overlay = pygame.Surface((LARGURA_TELA, ALTURA_TELA), pygame.SRCALPHA)
    overlay.fill((10, 12, 25, 200))
    tela.blit(overlay, (0, 0))

    # --- Fontes ---
    fonte_titulo = pygame.font.SysFont("arial", 52, bold=True)
    fonte_sub    = pygame.font.SysFont("arial", 22, bold=True)
    fonte_valor  = pygame.font.SysFont("arial", 36, bold=True)
    fonte_label  = pygame.font.SysFont("arial", 18)
    fonte_rodape = pygame.font.SysFont("arial", 20)

    cx = LARGURA_TELA // 2
    cy = ALTURA_TELA // 2

    # --- Painel central ---
    painel_w, painel_h = 560, 340
    painel_x = cx - painel_w // 2
    painel_y = cy - painel_h // 2 - 10
    _desenhar_card(tela, painel_x, painel_y, painel_w, painel_h)

    # --- Título ---
    _desenhar_texto(tela, "VOCÊ VENCEU!", fonte_titulo, DOURADO, (cx, painel_y + 52))

    # --- Estrelas ---
    _desenhar_estrelas(tela, cx, painel_y + 82, n=3)

    # --- Separador ---
    sep_y = painel_y + 116
    pygame.draw.line(tela, BORDA_CARD, (painel_x + 30, sep_y), (painel_x + painel_w - 30, sep_y), 1)

    # --- Cards de estatísticas ---
    card_w, card_h = 148, 90
    espaco_cards = 18
    total_cards = 3 * card_w + 2 * espaco_cards
    card_inicio_x = cx - total_cards // 2
    card_y = sep_y + 18

    stats = [
        ("PONTOS",  str(estado["pontos"]),  CARTA_ENCONTRADA),
        ("TEMPO",   f"{tempo_gasto}s",       LARANJA),
        ("RECORDE", str(recorde),            DOURADO),
    ]

    for i, (label, valor, cor_valor) in enumerate(stats):
        cx_card = card_inicio_x + i * (card_w + espaco_cards)

        mini = pygame.Surface((card_w, card_h), pygame.SRCALPHA)
        pygame.draw.rect(mini, (30, 34, 58, 200), (0, 0, card_w, card_h), border_radius=10)
        pygame.draw.rect(mini, (*cor_valor, 80), (0, 0, card_w, card_h), width=2, border_radius=10)
        tela.blit(mini, (cx_card, card_y))

        _desenhar_texto(tela, label, fonte_label, CINZA, (cx_card + card_w // 2, card_y + 24))
        _desenhar_texto(tela, valor, fonte_valor, cor_valor, (cx_card + card_w // 2, card_y + 62))

    # --- Badge "NOVO RECORDE!" ---
    if novo_recorde:
        badge_y = card_y + card_h + 22
        badge_w, badge_h = 220, 34
        badge_surf = pygame.Surface((badge_w, badge_h), pygame.SRCALPHA)
        pygame.draw.rect(badge_surf, (*DOURADO, 40), (0, 0, badge_w, badge_h), border_radius=17)
        pygame.draw.rect(badge_surf, (*DOURADO, 180), (0, 0, badge_w, badge_h), width=2, border_radius=17)
        tela.blit(badge_surf, (cx - badge_w // 2, badge_y))
        _desenhar_texto(tela, "⭐  NOVO RECORDE!  ⭐", fonte_sub, DOURADO, (cx, badge_y + badge_h // 2))

    # --- Rodapé ---
    rodape_y = painel_y + painel_h - 26
    _desenhar_texto(
        tela,
        "Pressione  R  para jogar novamente   |   ESC  para sair",
        fonte_rodape,
        CINZA,
        (cx, rodape_y),
    )