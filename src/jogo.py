import pygame

from src.config import (
    LARGURA_TELA,
    ALTURA_TELA,
    FPS,
    TITULO_JOGO,
    MARGEM,
    ESPACO_TOPO,
    PONTOS_POR_PAR,
    PONTOS_POR_SEGUNDO,
    ATRASO_ERRO,
    SIMBOLOS,
    NIVEIS,
    NIVEL_PADRAO,
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
from src.dados import carregar_recordes, salvar_recordes
from src.tela_vitoria import desenhar_tela_vitoria


# Margens da área do tabuleiro (usadas para calcular o tamanho das cartas)
MARGEM_LATERAL = 40
MARGEM_INFERIOR = 30


# ---------------------------------------------------------------------------
# Tabuleiro e estado
# ---------------------------------------------------------------------------

def criar_tabuleiro(linhas, colunas):
    """Cria as cartas de uma grade linhas x colunas, ajustando o tamanho das
    cartas para caber na tela. Devolve (tabuleiro, tamanho_da_carta)."""
    largura_disp = LARGURA_TELA - 2 * MARGEM_LATERAL
    altura_disp = ALTURA_TELA - ESPACO_TOPO - MARGEM_INFERIOR

    # Maior carta quadrada que cabe na grade, considerando as margens.
    carta_por_largura = (largura_disp - (colunas - 1) * MARGEM) / colunas
    carta_por_altura = (altura_disp - (linhas - 1) * MARGEM) / linhas
    tamanho = int(min(carta_por_largura, carta_por_altura))

    largura_grade = colunas * tamanho + (colunas - 1) * MARGEM
    altura_grade = linhas * tamanho + (linhas - 1) * MARGEM
    inicio_x = (LARGURA_TELA - largura_grade) // 2
    inicio_y = ESPACO_TOPO + (altura_disp - altura_grade) // 2

    numero_pares = (linhas * colunas) // 2
    valores = criar_valores_embaralhados(SIMBOLOS[:numero_pares])

    tabuleiro = []
    for indice, valor in enumerate(valores):
        linha, coluna = indice_para_coordenada(indice, colunas)
        x = inicio_x + coluna * (tamanho + MARGEM)
        y = inicio_y + linha * (tamanho + MARGEM)

        carta = {
            "valor": valor,
            "posicao": (linha, coluna),
            "rect": pygame.Rect(x, y, tamanho, tamanho),
            "revelada": False,
            "encontrada": False,
        }
        tabuleiro.append(carta)

    return tabuleiro, tamanho


def estado_inicial(nivel=NIVEL_PADRAO):
    """Devolve o estado de uma nova partida para o nível informado."""
    cfg = NIVEIS[nivel]
    tabuleiro, tamanho = criar_tabuleiro(cfg["linhas"], cfg["colunas"])

    return {
        "tabuleiro": tabuleiro,
        "tamanho_carta": tamanho,
        "nivel": nivel,
        "numero_pares": (cfg["linhas"] * cfg["colunas"]) // 2,
        "tempo_limite": cfg["tempo"],
        "peso": cfg["peso"],
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


def _fonte_carta(tamanho):
    """Cria a fonte das cartas proporcional ao tamanho da carta."""
    return pygame.font.SysFont("arial", max(20, int(tamanho * 0.55)), bold=True)


def iniciar_partida(nivel):
    """Inicia uma partida no nível dado e devolve (estado, fonte_carta)."""
    estado = estado_inicial(nivel)
    estado["situacao"] = "jogando"
    estado["inicio"] = pygame.time.get_ticks()
    return estado, _fonte_carta(estado["tamanho_carta"])


# ---------------------------------------------------------------------------
# Lógica de jogo
# ---------------------------------------------------------------------------

def tempo_restante(estado):
    """Calcula quantos segundos ainda restam, descontando o tempo em pausa."""
    decorrido = (pygame.time.get_ticks() - estado["inicio"] - estado["tempo_pausado"]) // 1000
    return max(0, estado["tempo_limite"] - decorrido)


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
        estado["pontos"] = calcular_pontos(estado["pontos"], PONTOS_POR_PAR * estado["peso"])
        estado["selecionadas"] = []

        if todos_pares_encontrados(estado["pares_encontrados"], estado["numero_pares"]):
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

def desenhar_menu(tela, recordes, fonte_titulo, fonte_botao, fonte_hud, fonte_rec, mouse_pos):
    """Renderiza o menu inicial e devolve um dicionário com os rects clicáveis."""
    tela.fill(FUNDO)

    desenhar_texto(tela, "MemoryPy", fonte_titulo, AMARELO,
                   (LARGURA_TELA // 2, 100))
    desenhar_texto(tela, "Escolha a dificuldade", fonte_hud, CINZA,
                   (LARGURA_TELA // 2, 150))

    largura_btn, altura_btn = 180, 50
    cx = LARGURA_TELA // 2
    x_esq = cx - 100
    x_dir = cx + 100

    posicoes = {
        "facil":   (x_esq, 250),
        "medio":   (x_dir, 250),
        "dificil": (x_esq, 330),
        "extremo": (x_dir, 330),
    }

    rects = {}
    for nivel, (px, py) in posicoes.items():
        rect = pygame.Rect(0, 0, largura_btn, altura_btn)
        rect.center = (px, py)
        cfg = NIVEIS[nivel]
        _desenhar_botao(tela, f"{cfg['rotulo']} ({cfg['tempo']}s)", fonte_botao, rect, mouse_pos)
        rec = recordes.get(nivel, 0)
        desenhar_texto(tela, f"Recorde: {rec}", fonte_rec, CINZA, (px, py + 36))
        rects[nivel] = rect

    rect_sair = pygame.Rect(0, 0, largura_btn, altura_btn)
    rect_sair.center = (cx, 420)
    _desenhar_botao(tela, "Sair", fonte_botao, rect_sair, mouse_pos)
    rects["sair"] = rect_sair

    desenhar_texto(tela, "Durante o jogo:  P pausa   R reinicia   ESC sai",
                   fonte_hud, CINZA, (LARGURA_TELA // 2, 505))

    return rects


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

    rotulo = NIVEIS[estado["nivel"]]["rotulo"]
    desenhar_texto(tela, f"Nivel: {rotulo}    P: pausar    R: reiniciar    ESC: sair",
                   fonte_hud, CINZA, (LARGURA_TELA // 2, 70))


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

    fonte_hud    = pygame.font.SysFont("arial", 22)
    fonte_fim    = pygame.font.SysFont("arial", 40, bold=True)
    fonte_titulo = pygame.font.SysFont("arial", 64, bold=True)
    fonte_botao  = pygame.font.SysFont("arial", 24, bold=True)
    fonte_rec    = pygame.font.SysFont("arial", 16)

    recordes = carregar_recordes(CAMINHO_RECORDE)
    estado = estado_inicial(NIVEL_PADRAO)          # começa no menu
    fonte_carta = _fonte_carta(estado["tamanho_carta"])

    rodando = True
    while rodando:
        relogio.tick(FPS)
        mouse_pos = pygame.mouse.get_pos()
        situacao = estado["situacao"]

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
                    estado, fonte_carta = iniciar_partida(estado["nivel"])

                elif evento.key == pygame.K_m and situacao in ("vitoria", "derrota", "pausado"):
                    estado = estado_inicial(NIVEL_PADRAO)   # volta ao menu

            elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:

                if situacao == "menu":
                    rects = desenhar_menu(
                        tela, recordes, fonte_titulo, fonte_botao, fonte_hud, fonte_rec, mouse_pos
                    )
                    clicou_nivel = False
                    for nivel in NIVEIS:
                        if rects[nivel].collidepoint(mouse_pos):
                            estado, fonte_carta = iniciar_partida(nivel)
                            clicou_nivel = True
                            break
                    if not clicou_nivel and rects["sair"].collidepoint(mouse_pos):
                        rodando = False

                elif situacao == "pausado":
                    rect_retomar, rect_menu, rect_sair = desenhar_pausa(
                        tela, fonte_titulo, fonte_botao, fonte_hud, mouse_pos
                    )
                    if rect_retomar.collidepoint(mouse_pos):
                        retomar(estado)
                    elif rect_menu.collidepoint(mouse_pos):
                        estado = estado_inicial(NIVEL_PADRAO)
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
                ) * estado["peso"]
                estado["bonus_tempo"] = bonus
                estado["pontos"] = calcular_pontos(estado["pontos"], bonus)

                nivel = estado["nivel"]
                if eh_novo_recorde(estado["pontos"], recordes.get(nivel, 0)):
                    recordes[nivel] = estado["pontos"]
                    salvar_recordes(CAMINHO_RECORDE, recordes)
                    estado["novo_recorde"] = True

        # --- Renderização ---
        if situacao == "menu":
            desenhar_menu(tela, recordes, fonte_titulo, fonte_botao, fonte_hud, fonte_rec, mouse_pos)

        else:
            tela.fill(FUNDO)
            for carta in estado["tabuleiro"]:
                desenhar_carta(tela, carta, fonte_carta)
            recorde_nivel = recordes.get(estado["nivel"], 0)
            desenhar_placar(tela, estado, recorde_nivel, fonte_hud)

            if situacao == "pausado":
                desenhar_pausa(tela, fonte_titulo, fonte_botao, fonte_hud, mouse_pos)
            elif situacao == "vitoria":
                desenhar_tela_vitoria(tela, estado, recorde_nivel, estado["novo_recorde"], estado["tempo_vitoria"])
            elif situacao == "derrota":
                desenhar_fim(tela, estado, fonte_fim)

        pygame.display.flip()

    pygame.quit()