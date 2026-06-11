import pygame

from src.config import (
    LARGURA_TELA,
    ALTURA_TELA,
    FPS,
    TITULO_JOGO,
    LINHAS,
    COLUNAS,
    NUMERO_PARES,
    TAMANHO_CARTA,
    MARGEM,
    ESPACO_TOPO,
    TEMPO_LIMITE,
    PONTOS_POR_PAR,
    PONTOS_POR_SEGUNDO,
    ATRASO_ERRO,
    SIMBOLOS,
    FUNDO,
    TEXTO_CLARO,
    CARTA_ENCONTRADA,
    CINZA,
    CAMINHO_RECORDE,
    BOTAO_FUNDO,
    BOTAO_HOVER,
    BOTAO_BORDA,
    AMARELO,
)
from src.funcoes import (
    criar_valores_embaralhados,
    indice_para_coordenada,
    verificar_par,
    calcular_pontos,
    calcular_bonus_tempo,
    todos_pares_encontrados,
    eh_novo_recorde,
)
from src.sprites import desenhar_carta, desenhar_texto
from src.dados import carregar_recorde, salvar_recorde
from src.tela_vitoria import desenhar_tela_vitoria


# ---------------------------------------------------------------------------
# Tabuleiro e estado
# ---------------------------------------------------------------------------

def criar_tabuleiro():
    """Cria a lista de cartas do tabuleiro já posicionadas na tela."""
    valores = criar_valores_embaralhados(SIMBOLOS)

    largura_grade = COLUNAS * TAMANHO_CARTA + (COLUNAS - 1) * MARGEM
    inicio_x = (LARGURA_TELA - largura_grade) // 2
    inicio_y = ESPACO_TOPO

    tabuleiro = []
    for indice, valor in enumerate(valores):
        linha, coluna = indice_para_coordenada(indice, COLUNAS)
        x = inicio_x + coluna * (TAMANHO_CARTA + MARGEM)
        y = inicio_y + linha * (TAMANHO_CARTA + MARGEM)

        carta = {
            "valor": valor,
            "posicao": (linha, coluna),
            "rect": pygame.Rect(x, y, TAMANHO_CARTA, TAMANHO_CARTA),
            "revelada": False,
            "encontrada": False,
        }
        tabuleiro.append(carta)

    return tabuleiro


def estado_inicial():
    """Devolve um dicionário com todo o estado de uma nova partida."""
    return {
        "tabuleiro": criar_tabuleiro(),
        "selecionadas": [],
        "pares_encontrados": set(),
        "tentativas": 0,
        "pontos": 0,
        "bonus_tempo": 0,        # bônus ganho pelo tempo ao vencer
        "inicio": pygame.time.get_ticks(),
        "tempo_pausado": 0,      # ms acumulados em pausa
        "inicio_pausa": None,    # momento em que a pausa começou
        "erro_em": None,
        "situacao": "menu",      # "menu", "jogando", "pausado", "vitoria", "derrota"
        "tempo_vitoria": 0,      # segundos restantes no momento da vitória
        "novo_recorde": False,   # True se esta partida bateu o recorde
    }


# ---------------------------------------------------------------------------
# Lógica de jogo
# ---------------------------------------------------------------------------

def tempo_restante(estado):
    """Calcula quantos segundos ainda restam, descontando o tempo em pausa."""
    decorrido = (pygame.time.get_ticks() - estado["inicio"] - estado["tempo_pausado"]) // 1000
    return max(0, TEMPO_LIMITE - decorrido)


def pausar(estado):
    """Registra o instante em que a pausa começou."""
    estado["inicio_pausa"] = pygame.time.get_ticks()
    estado["situacao"] = "pausado"


def retomar(estado):
    """Acumula o tempo que ficou pausado e volta a jogar."""
    if estado["inicio_pausa"] is not None:
        estado["tempo_pausado"] += pygame.time.get_ticks() - estado["inicio_pausa"]
        estado["inicio_pausa"] = None
    estado["situacao"] = "jogando"


def tratar_clique(estado, posicao_mouse):
    """Revela a carta clicada, respeitando as regras de turno."""
    if estado["erro_em"] is not None:
        return
    if len(estado["selecionadas"]) >= 2:
        return

    for indice, carta in enumerate(estado["tabuleiro"]):
        if carta["rect"].collidepoint(posicao_mouse):
            if carta["revelada"] or carta["encontrada"]:
                return
            carta["revelada"] = True
            estado["selecionadas"].append(indice)
            break


def avaliar_jogada(estado):
    """Quando duas cartas estão viradas, verifica se formam um par."""
    if len(estado["selecionadas"]) != 2 or estado["erro_em"] is not None:
        return

    estado["tentativas"] += 1
    indice_a, indice_b = estado["selecionadas"]
    carta_a = estado["tabuleiro"][indice_a]
    carta_b = estado["tabuleiro"][indice_b]

    if verificar_par(carta_a["valor"], carta_b["valor"]):
        carta_a["encontrada"] = True
        carta_b["encontrada"] = True
        estado["pares_encontrados"].add(carta_a["valor"])
        estado["pontos"] = calcular_pontos(estado["pontos"], PONTOS_POR_PAR)
        estado["selecionadas"] = []

        if todos_pares_encontrados(estado["pares_encontrados"], NUMERO_PARES):
            estado["situacao"] = "vitoria"
            estado["tempo_vitoria"] = tempo_restante(estado)
    else:
        estado["erro_em"] = pygame.time.get_ticks()


def atualizar_erro(estado):
    """Após a pausa, vira de volta as duas cartas que não formaram par."""
    if estado["erro_em"] is None:
        return
    if pygame.time.get_ticks() - estado["erro_em"] >= ATRASO_ERRO:
        for indice in estado["selecionadas"]:
            estado["tabuleiro"][indice]["revelada"] = False
        estado["selecionadas"] = []
        estado["erro_em"] = None


# ---------------------------------------------------------------------------
# Helpers de desenho
# ---------------------------------------------------------------------------

def _overlay(tela, alpha=180):
    """Desenha um overlay escuro semi-transparente sobre a tela inteira."""
    fundo = pygame.Surface((LARGURA_TELA, ALTURA_TELA))
    fundo.set_alpha(alpha)
    fundo.fill((0, 0, 0))
    tela.blit(fundo, (0, 0))


def _desenhar_botao(tela, texto, fonte, rect, mouse_pos):
    """Desenha um botão e retorna True se o mouse estiver sobre ele."""
    hover = rect.collidepoint(mouse_pos)
    cor_fundo = BOTAO_HOVER if hover else BOTAO_FUNDO
    pygame.draw.rect(tela, cor_fundo, rect, border_radius=10)
    pygame.draw.rect(tela, BOTAO_BORDA, rect, width=2, border_radius=10)
    desenhar_texto(tela, texto, fonte, TEXTO_CLARO, rect.center)
    return hover


# ---------------------------------------------------------------------------
# Telas
# ---------------------------------------------------------------------------

def desenhar_menu(tela, recorde, fonte_titulo, fonte_botao, fonte_hud, mouse_pos):
    """Renderiza o menu inicial e devolve os rects dos botões."""
    tela.fill(FUNDO)

    desenhar_texto(tela, "MemoryPy", fonte_titulo, AMARELO,
                   (LARGURA_TELA // 2, 140))
    desenhar_texto(tela, "Jogo da Memoria em Python", fonte_hud, CINZA,
                   (LARGURA_TELA // 2, 200))
    desenhar_texto(tela, f"Recorde: {recorde}", fonte_hud, TEXTO_CLARO,
                   (LARGURA_TELA // 2, 250))

    largura_btn, altura_btn = 220, 55
    cx = LARGURA_TELA // 2

    rect_jogar = pygame.Rect(0, 0, largura_btn, altura_btn)
    rect_jogar.center = (cx, 340)

    rect_sair = pygame.Rect(0, 0, largura_btn, altura_btn)
    rect_sair.center = (cx, 420)

    _desenhar_botao(tela, "Jogar", fonte_botao, rect_jogar, mouse_pos)
    _desenhar_botao(tela, "Sair", fonte_botao, rect_sair, mouse_pos)

    desenhar_texto(tela, "P: pausar    R: reiniciar    ESC: sair", fonte_hud, CINZA,
                   (LARGURA_TELA // 2, 510))

    return rect_jogar, rect_sair


def desenhar_pausa(tela, fonte_titulo, fonte_botao, fonte_hud, mouse_pos):
    """Renderiza o overlay de pausa e devolve os rects dos botões."""
    _overlay(tela, alpha=200)

    desenhar_texto(tela, "Pausado", fonte_titulo, AMARELO,
                   (LARGURA_TELA // 2, ALTURA_TELA // 2 - 120))

    largura_btn, altura_btn = 220, 55
    cx = LARGURA_TELA // 2

    rect_retomar = pygame.Rect(0, 0, largura_btn, altura_btn)
    rect_retomar.center = (cx, ALTURA_TELA // 2 - 20)

    rect_menu = pygame.Rect(0, 0, largura_btn, altura_btn)
    rect_menu.center = (cx, ALTURA_TELA // 2 + 60)

    rect_sair = pygame.Rect(0, 0, largura_btn, altura_btn)
    rect_sair.center = (cx, ALTURA_TELA // 2 + 140)

    _desenhar_botao(tela, "Retomar (P)", fonte_botao, rect_retomar, mouse_pos)
    _desenhar_botao(tela, "Menu", fonte_botao, rect_menu, mouse_pos)
    _desenhar_botao(tela, "Sair", fonte_botao, rect_sair, mouse_pos)

    return rect_retomar, rect_menu, rect_sair


def desenhar_placar(tela, estado, recorde, fonte_hud):
    """Mostra tentativas, pontos, tempo e recorde no topo da tela."""
    desenhar_texto(tela, f"Tentativas: {estado['tentativas']}", fonte_hud, TEXTO_CLARO, (120, 30))
    desenhar_texto(tela, f"Pontos: {estado['pontos']}", fonte_hud, TEXTO_CLARO, (340, 30))
    desenhar_texto(tela, f"Tempo: {tempo_restante(estado)}s", fonte_hud, TEXTO_CLARO, (520, 30))
    desenhar_texto(tela, f"Recorde: {recorde}", fonte_hud, TEXTO_CLARO, (690, 30))
    desenhar_texto(tela, "P: pausar    R: reiniciar    ESC: sair", fonte_hud, CINZA,
                   (LARGURA_TELA // 2, 70))


def desenhar_fim(tela, estado, fonte_fim):
    """Tela de derrota (tempo esgotado). A vitória usa desenhar_tela_vitoria."""
    _overlay(tela)
    desenhar_texto(tela, "Tempo esgotado!", fonte_fim, CARTA_ENCONTRADA,
                   (LARGURA_TELA // 2, ALTURA_TELA // 2 - 20))
    desenhar_texto(tela, "R: jogar de novo    M: menu", fonte_fim, TEXTO_CLARO,
                   (LARGURA_TELA // 2, ALTURA_TELA // 2 + 40))


# ---------------------------------------------------------------------------
# Loop principal
# ---------------------------------------------------------------------------

def executar_jogo():
    """Inicializa o Pygame e executa o loop principal do jogo da memória."""
    pygame.init()
    tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
    pygame.display.set_caption(TITULO_JOGO)
    relogio = pygame.time.Clock()

    fonte_carta  = pygame.font.SysFont("arial", 48, bold=True)
    fonte_hud    = pygame.font.SysFont("arial", 22)
    fonte_fim    = pygame.font.SysFont("arial", 40, bold=True)
    fonte_titulo = pygame.font.SysFont("arial", 64, bold=True)
    fonte_botao  = pygame.font.SysFont("arial", 28, bold=True)

    recorde = carregar_recorde(CAMINHO_RECORDE)
    estado  = estado_inicial()   # começa no menu

    rodando = True
    while rodando:
        relogio.tick(FPS)
        mouse_pos = pygame.mouse.get_pos()
        situacao  = estado["situacao"]

        # --- Eventos ---
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    if situacao == "jogando":
                        pausar(estado)
                    else:
                        rodando = False

                elif evento.key == pygame.K_p and situacao == "jogando":
                    pausar(estado)

                elif evento.key == pygame.K_p and situacao == "pausado":
                    retomar(estado)

                elif evento.key == pygame.K_r and situacao in ("jogando", "vitoria", "derrota"):
                    estado = estado_inicial()
                    estado["situacao"] = "jogando"
                    estado["inicio"] = pygame.time.get_ticks()

                elif evento.key == pygame.K_m and situacao in ("vitoria", "derrota", "pausado"):
                    estado = estado_inicial()   # volta ao menu

            elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:

                if situacao == "menu":
                    rect_jogar, rect_sair = desenhar_menu(
                        tela, recorde, fonte_titulo, fonte_botao, fonte_hud, mouse_pos
                    )
                    if rect_jogar.collidepoint(mouse_pos):
                        estado = estado_inicial()
                        estado["situacao"] = "jogando"
                        estado["inicio"] = pygame.time.get_ticks()
                    elif rect_sair.collidepoint(mouse_pos):
                        rodando = False

                elif situacao == "pausado":
                    rect_retomar, rect_menu, rect_sair = desenhar_pausa(
                        tela, fonte_titulo, fonte_botao, fonte_hud, mouse_pos
                    )
                    if rect_retomar.collidepoint(mouse_pos):
                        retomar(estado)
                    elif rect_menu.collidepoint(mouse_pos):
                        estado = estado_inicial()
                    elif rect_sair.collidepoint(mouse_pos):
                        rodando = False

                elif situacao == "jogando":
                    tratar_clique(estado, mouse_pos)

        # --- Atualização do estado ---
        if situacao == "jogando":
            avaliar_jogada(estado)
            atualizar_erro(estado)

            if tempo_restante(estado) <= 0:
                estado["situacao"] = "derrota"

            if estado["situacao"] == "vitoria":
                bonus = calcular_bonus_tempo(
                    estado["tempo_vitoria"], PONTOS_POR_SEGUNDO
                )
                estado["bonus_tempo"] = bonus
                estado["pontos"] = calcular_pontos(estado["pontos"], bonus)

                if eh_novo_recorde(estado["pontos"], recorde):
                    recorde = estado["pontos"]
                    salvar_recorde(CAMINHO_RECORDE, recorde)
                    estado["novo_recorde"] = True

        # --- Renderização ---
        if situacao == "menu":
            desenhar_menu(tela, recorde, fonte_titulo, fonte_botao, fonte_hud, mouse_pos)

        else:
            tela.fill(FUNDO)
            for carta in estado["tabuleiro"]:
                desenhar_carta(tela, carta, fonte_carta)
            desenhar_placar(tela, estado, recorde, fonte_hud)

            if situacao == "pausado":
                desenhar_pausa(tela, fonte_titulo, fonte_botao, fonte_hud, mouse_pos)
            elif situacao == "vitoria":
                desenhar_tela_vitoria(tela, estado, recorde, estado["novo_recorde"], estado["tempo_vitoria"])
            elif situacao == "derrota":
                desenhar_fim(tela, estado, fonte_fim)

        pygame.display.flip()

    pygame.quit()