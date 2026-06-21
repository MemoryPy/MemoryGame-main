# Este arquivo desenha as telas que aparecem quando a partida e vencida.
# No modo 1 jogador, um painel mostra os pontos, o tempo, o recorde, a
# precisao, as estatisticas pessoais, as conquistas novas e o ranking (com
# campo para digitar o nome, se a pontuacao entrar no top 5). No modo 2
# jogadores, uma tela mais simples so compara a pontuacao dos dois. E so
# parte visual, nao tem regra de jogo aqui.

import math

import pygame

from src.config import (
    LARGURA_TELA,
    ALTURA_TELA,
    CONQUISTAS_LABELS,
)


# Cores usadas so nesta tela (as outras vem do tema, passado por parametro).
DOURADO = (255, 215, 60)
DOURADO_ESCURO = (200, 160, 0)
AZUL_CARD = (45, 50, 75)
BORDA_CARD = (80, 90, 130)
VERDE_CLARO = (160, 230, 170)
LARANJA = (255, 160, 50)
AZUL_JOGADOR = (90, 160, 230)
ROSA_JOGADOR = (230, 110, 160)


def _desenhar_texto(tela, texto, fonte, cor, centro):
    """Escreve um texto centralizado (atalho usado varias vezes nesta tela)."""
    sup = fonte.render(texto, True, cor)
    ret = sup.get_rect(center=centro)
    tela.blit(sup, ret)


def _desenhar_card(tela, x, y, largura, altura):
    """Desenha o painel de fundo (caixa arredondada meio transparente)."""
    surf = pygame.Surface((largura, altura), pygame.SRCALPHA)
    pygame.draw.rect(surf, (*AZUL_CARD, 220), (0, 0, largura, altura), border_radius=14)
    pygame.draw.rect(surf, (*BORDA_CARD, 180), (0, 0, largura, altura), width=2, border_radius=14)
    tela.blit(surf, (x, y))


def _desenhar_estrelas(tela, cx, y, n=3):
    """Desenha varias estrelas douradas lado a lado, so para enfeitar."""
    tamanho = 22
    espaco = 14
    total = n * tamanho + (n - 1) * espaco
    inicio_x = cx - total // 2

    for i in range(n):
        sx = inicio_x + i * (tamanho + espaco) + tamanho // 2
        _desenhar_estrela(tela, sx, y + tamanho // 2, tamanho // 2, DOURADO)


def _desenhar_estrela(tela, cx, cy, raio, cor):
    """Desenha uma unica estrela de 5 pontas usando um pouco de matematica
    para achar as pontas em volta de um circulo."""
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


def desenhar_tela_vitoria(tela, estado, recorde, novo_recorde, tempo_gasto,
                           estatisticas_nivel, conquistas_novas, ranking_nivel,
                           entrada_nome, pedindo_nome):
    """Desenha a tela de vitoria por cima do tabuleiro (modo 1 jogador).

    Mostra os pontos, o tempo, o recorde, a precisao da partida, as
    melhores estatisticas pessoais do nivel, as conquistas novas e o
    ranking (com um campo para digitar o nome, se a pontuacao entrar nele).
    """
    overlay = pygame.Surface((LARGURA_TELA, ALTURA_TELA), pygame.SRCALPHA)
    overlay.fill((10, 12, 25, 200))
    tela.blit(overlay, (0, 0))

    fonte_titulo = pygame.font.SysFont("arial", 44, bold=True)
    fonte_sub    = pygame.font.SysFont("arial", 19, bold=True)
    fonte_valor  = pygame.font.SysFont("arial", 28, bold=True)
    fonte_label  = pygame.font.SysFont("arial", 15)
    fonte_rodape = pygame.font.SysFont("arial", 17)
    fonte_lista  = pygame.font.SysFont("arial", 16)

    cx = LARGURA_TELA // 2

    painel_w, painel_h = 620, 470
    painel_x = cx - painel_w // 2
    painel_y = 35
    _desenhar_card(tela, painel_x, painel_y, painel_w, painel_h)

    _desenhar_texto(tela, "VOCÊ VENCEU!", fonte_titulo, DOURADO, (cx, painel_y + 38))
    _desenhar_estrelas(tela, cx, painel_y + 62, n=3)

    sep_y = painel_y + 92
    pygame.draw.line(tela, BORDA_CARD, (painel_x + 30, sep_y), (painel_x + painel_w - 30, sep_y), 1)

    # --- Cards de estatísticas da partida ---
    card_w, card_h = 132, 76
    espaco_cards = 14
    total_cards = 4 * card_w + 3 * espaco_cards
    card_inicio_x = cx - total_cards // 2
    card_y = sep_y + 14

    stats = [
        ("PONTOS",   str(estado["pontos"]),              VERDE_CLARO),
        ("TEMPO",    f"{tempo_gasto}s",                   LARANJA),
        ("RECORDE",  str(recorde),                        DOURADO),
        ("PRECISÃO", f"{estado.get('precisao', 0)}%",     AZUL_JOGADOR),
    ]

    for i, (label, valor, cor_valor) in enumerate(stats):
        cx_card = card_inicio_x + i * (card_w + espaco_cards)

        mini = pygame.Surface((card_w, card_h), pygame.SRCALPHA)
        pygame.draw.rect(mini, (30, 34, 58, 200), (0, 0, card_w, card_h), border_radius=10)
        pygame.draw.rect(mini, (*cor_valor, 80), (0, 0, card_w, card_h), width=2, border_radius=10)
        tela.blit(mini, (cx_card, card_y))

        _desenhar_texto(tela, label, fonte_label, (200, 200, 210), (cx_card + card_w // 2, card_y + 20))
        _desenhar_texto(tela, valor, fonte_valor, cor_valor, (cx_card + card_w // 2, card_y + 50))

    proxima_y = card_y + card_h + 14

    if novo_recorde:
        badge_w, badge_h = 200, 30
        badge_surf = pygame.Surface((badge_w, badge_h), pygame.SRCALPHA)
        pygame.draw.rect(badge_surf, (*DOURADO, 40), (0, 0, badge_w, badge_h), border_radius=15)
        pygame.draw.rect(badge_surf, (*DOURADO, 180), (0, 0, badge_w, badge_h), width=2, border_radius=15)
        tela.blit(badge_surf, (cx - badge_w // 2, proxima_y))
        _desenhar_texto(tela, "NOVO RECORDE!", fonte_sub, DOURADO, (cx, proxima_y + badge_h // 2))
        proxima_y += badge_h + 10

    # --- Estatísticas pessoais do nível ---
    melhor_tempo = estatisticas_nivel.get("melhor_tempo")
    if melhor_tempo is None:
        melhor_tempo = "-"

    menor_tentativas = estatisticas_nivel.get("menor_tentativas")
    if menor_tentativas is None:
        menor_tentativas = "-"

    partidas = estatisticas_nivel.get("partidas", 0)
    texto_stats = (
        f"Melhor tempo restante: {melhor_tempo}s   |   "
        f"Menos tentativas: {menor_tentativas}   |   "
        f"Partidas jogadas: {partidas}"
    )
    _desenhar_texto(tela, texto_stats, fonte_label, (190, 195, 210), (cx, proxima_y + 10))
    proxima_y += 28

    # --- Conquistas novas ---
    if conquistas_novas:
        texto_conquistas = "Conquista desbloqueada: "
        primeira = True
        for chave in conquistas_novas:
            if not primeira:
                texto_conquistas += " | "
            texto_conquistas += CONQUISTAS_LABELS.get(chave, chave)
            primeira = False

        _desenhar_texto(tela, texto_conquistas, fonte_label, DOURADO, (cx, proxima_y + 8))
        proxima_y += 26

    # --- Ranking ou campo para digitar o nome ---
    pygame.draw.line(tela, BORDA_CARD, (painel_x + 30, proxima_y + 6), (painel_x + painel_w - 30, proxima_y + 6), 1)
    proxima_y += 18

    if pedindo_nome:
        _desenhar_texto(tela, "Sua pontuação entrou no ranking! Digite seu nome:",
                        fonte_label, (220, 220, 230), (cx, proxima_y + 6))
        caixa = pygame.Rect(0, 0, 260, 32)
        caixa.center = (cx, proxima_y + 38)
        pygame.draw.rect(tela, (30, 34, 58), caixa, border_radius=6)
        pygame.draw.rect(tela, DOURADO, caixa, width=2, border_radius=6)
        _desenhar_texto(tela, entrada_nome + "|", fonte_lista, (235, 235, 245), caixa.center)
        _desenhar_texto(tela, "Pressione ENTER para confirmar", fonte_label,
                        (180, 185, 200), (cx, proxima_y + 64))
    else:
        _desenhar_texto(tela, f"Ranking — {estado['nivel'].capitalize()}", fonte_label,
                        (200, 200, 210), (cx, proxima_y + 6))
        if ranking_nivel:
            for i, item in enumerate(ranking_nivel[:5]):
                _desenhar_texto(
                    tela,
                    f"{i + 1}. {item['nome']} — {item['pontos']} pts",
                    fonte_lista, (225, 225, 235), (cx, proxima_y + 30 + i * 22),
                )
        else:
            _desenhar_texto(tela, "Ainda não há nomes no ranking deste nível.",
                            fonte_lista, (180, 185, 200), (cx, proxima_y + 30))

    rodape_y = painel_y + painel_h - 22
    _desenhar_texto(
        tela,
        "Pressione  R  para jogar novamente   |   M  para o menu   |   ESC  para sair",
        fonte_rodape,
        (200, 205, 215),
        (cx, rodape_y),
    )


def desenhar_tela_vitoria_2p(tela, estado):
    """Desenha a tela de fim de partida do modo 2 jogadores: compara a
    pontuação dos dois jogadores e mostra quem venceu (ou se empatou).

    O modo 2 jogadores não usa recorde, ranking, estatísticas pessoais nem
    conquistas: a pontuação vale só para esta partida, entre os dois.
    """
    overlay = pygame.Surface((LARGURA_TELA, ALTURA_TELA), pygame.SRCALPHA)
    overlay.fill((10, 12, 25, 200))
    tela.blit(overlay, (0, 0))

    fonte_titulo = pygame.font.SysFont("arial", 44, bold=True)
    fonte_valor  = pygame.font.SysFont("arial", 34, bold=True)
    fonte_label  = pygame.font.SysFont("arial", 18)
    fonte_rodape = pygame.font.SysFont("arial", 18)

    cx = LARGURA_TELA // 2
    cy = ALTURA_TELA // 2

    painel_w, painel_h = 480, 300
    painel_x = cx - painel_w // 2
    painel_y = cy - painel_h // 2
    _desenhar_card(tela, painel_x, painel_y, painel_w, painel_h)

    pontos = estado["pontos_jogadores"]
    if pontos[0] > pontos[1]:
        titulo, cor_titulo = "JOGADOR 1 VENCEU!", AZUL_JOGADOR
    elif pontos[1] > pontos[0]:
        titulo, cor_titulo = "JOGADOR 2 VENCEU!", ROSA_JOGADOR
    else:
        titulo, cor_titulo = "EMPATE!", DOURADO

    _desenhar_texto(tela, titulo, fonte_titulo, cor_titulo, (cx, painel_y + 50))

    placar_y = painel_y + 130
    _desenhar_texto(tela, "Jogador 1", fonte_label, AZUL_JOGADOR, (cx - 110, placar_y))
    _desenhar_texto(tela, str(pontos[0]), fonte_valor, AZUL_JOGADOR, (cx - 110, placar_y + 36))
    _desenhar_texto(tela, "Jogador 2", fonte_label, ROSA_JOGADOR, (cx + 110, placar_y))
    _desenhar_texto(tela, str(pontos[1]), fonte_valor, ROSA_JOGADOR, (cx + 110, placar_y + 36))
    _desenhar_texto(tela, "×", fonte_valor, (200, 200, 210), (cx, placar_y + 18))

    rodape_y = painel_y + painel_h - 30
    _desenhar_texto(
        tela,
        "Pressione  R  para jogar novamente   |   M  para o menu",
        fonte_rodape,
        (200, 205, 215),
        (cx, rodape_y),
    )
