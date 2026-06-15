# Este e o arquivo principal do jogo. Ele junta tudo: cria o tabuleiro,
# controla o que acontece a cada clique e tecla, conta o tempo, decide
# vitoria ou derrota e manda desenhar cada tela. A funcao executar_jogo()
# la embaixo e o "motor" que fica rodando do inicio ao fim da partida.

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


# Espaco em branco deixado nas bordas da area onde ficam as cartas.
MARGEM_LATERAL = 40
MARGEM_INFERIOR = 30


# ---------------------------------------------------------------------------
# Montagem do tabuleiro e do estado da partida
# ---------------------------------------------------------------------------

def criar_tabuleiro(linhas, colunas):
    """Monta as cartas de uma grade do tamanho pedido.

    Calcula o tamanho de carta que cabe na tela, embaralha as letras e cria
    cada carta ja com sua posicao. Devolve a lista de cartas e o tamanho
    de carta usado (para a fonte combinar com o tamanho).
    """
    # Espaco que sobra na tela para colocar as cartas (tirando as margens).
    largura_disp = LARGURA_TELA - 2 * MARGEM_LATERAL
    altura_disp = ALTURA_TELA - ESPACO_TOPO - MARGEM_INFERIOR

    # Acha o maior tamanho de carta quadrada que ainda cabe na grade.
    carta_por_largura = (largura_disp - (colunas - 1) * MARGEM) / colunas
    carta_por_altura = (altura_disp - (linhas - 1) * MARGEM) / linhas
    tamanho = int(min(carta_por_largura, carta_por_altura))

    # Centraliza a grade na tela calculando onde a primeira carta comeca.
    largura_grade = colunas * tamanho + (colunas - 1) * MARGEM
    altura_grade = linhas * tamanho + (linhas - 1) * MARGEM
    inicio_x = (LARGURA_TELA - largura_grade) // 2
    inicio_y = ESPACO_TOPO + (altura_disp - altura_grade) // 2

    # Pega so as letras necessarias para o numero de pares deste tabuleiro.
    numero_pares = (linhas * colunas) // 2
    valores = criar_valores_embaralhados(SIMBOLOS[:numero_pares])

    # Cria cada carta como um dicionario, ja na sua posicao na tela.
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
    """Cria o "estado" da partida: um dicionario que guarda tudo que muda
    durante o jogo (cartas, pontos, tempo, situacao atual etc.).

    Manter tudo num so dicionario facilita reiniciar a partida: basta criar
    um estado novo. O jogo comeca na situacao "menu".
    """
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
    """Cria a fonte das letras das cartas, proporcional ao tamanho da carta
    (cartas menores, no nivel extremo, usam letras menores)."""
    return pygame.font.SysFont("arial", max(20, int(tamanho * 0.55)), bold=True)


def iniciar_partida(nivel):
    """Comeca de fato uma partida no nivel escolhido.

    Cria um estado novo, marca a situacao como "jogando" e zera o relogio.
    Devolve tambem a fonte das cartas, que depende do tamanho da grade.
    """
    estado = estado_inicial(nivel)
    estado["situacao"] = "jogando"
    estado["inicio"] = pygame.time.get_ticks()
    return estado, _fonte_carta(estado["tamanho_carta"])


# ---------------------------------------------------------------------------
# Regras que acontecem durante a partida
# ---------------------------------------------------------------------------

def tempo_restante(estado):
    """Diz quantos segundos ainda faltam para acabar a partida.

    Conta o tempo que passou desde o inicio, mas desconta o tempo em que o
    jogo ficou pausado, para a pausa nao "roubar" tempo do jogador.
    """
    decorrido = (pygame.time.get_ticks() - estado["inicio"] - estado["tempo_pausado"]) // 1000
    return max(0, estado["tempo_limite"] - decorrido)


def pausar(estado):
    """Pausa o jogo, anotando o momento em que a pausa comecou."""
    estado["inicio_pausa"] = pygame.time.get_ticks()
    estado["situacao"] = "pausado"


def retomar(estado):
    """Volta de uma pausa, somando quanto tempo o jogo ficou parado.

    Esse tempo somado depois e descontado em tempo_restante, para o
    cronometro continuar de onde parou.
    """
    if estado["inicio_pausa"] is not None:
        estado["tempo_pausado"] += pygame.time.get_ticks() - estado["inicio_pausa"]
        estado["inicio_pausa"] = None
    estado["situacao"] = "jogando"


def tratar_clique(estado, posicao_mouse):
    """Vira a carta que o jogador clicou.

    Ignora o clique se ja existem duas cartas viradas (esperando comparacao)
    ou se a carta clicada ja esta aberta. So vira cartas validas.
    """
    if estado["erro_em"] is not None:
        return
    if len(estado["selecionadas"]) >= 2:
        return

    # Procura entre as cartas qual delas o clique acertou.
    for indice, carta in enumerate(estado["tabuleiro"]):
        if carta["rect"].collidepoint(posicao_mouse):
            if carta["revelada"] or carta["encontrada"]:
                return
            carta["revelada"] = True
            estado["selecionadas"].append(indice)
            break


def avaliar_jogada(estado):
    """Compara as duas cartas viradas e decide o que acontece.

    Se forem iguais, viram um par (somam pontos e ficam abertas) e, se foi
    o ultimo par, a partida e vencida. Se forem diferentes, marca o momento
    para depois esconde-las de novo.
    """
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
    """Esconde de novo as duas cartas erradas depois de um tempinho.

    Quando o jogador erra, as cartas ficam visiveis por alguns instantes
    (ATRASO_ERRO) para ele decorar onde estao, e so depois viram de volta.
    """
    if estado["erro_em"] is None:
        return
    if pygame.time.get_ticks() - estado["erro_em"] >= ATRASO_ERRO:
        for indice in estado["selecionadas"]:
            estado["tabuleiro"][indice]["revelada"] = False
        estado["selecionadas"] = []
        estado["erro_em"] = None


# ---------------------------------------------------------------------------
# Pecas reutilizadas no desenho das telas
# ---------------------------------------------------------------------------

def _overlay(tela, alpha=180):
    """Joga uma camada escura por cima da tela (usada em pausa e derrota)
    para escurecer o fundo e destacar o texto que vem na frente."""
    fundo = pygame.Surface((LARGURA_TELA, ALTURA_TELA))
    fundo.set_alpha(alpha)
    fundo.fill((0, 0, 0))
    tela.blit(fundo, (0, 0))


def _desenhar_botao(tela, texto, fonte, rect, mouse_pos):
    """Desenha um botao na tela e muda a cor quando o mouse passa por cima.

    Devolve True se o mouse estiver em cima do botao, o que ajuda a saber
    se ele foi clicado.
    """
    hover = rect.collidepoint(mouse_pos)
    cor_fundo = BOTAO_HOVER if hover else BOTAO_FUNDO
    pygame.draw.rect(tela, cor_fundo, rect, border_radius=10)
    pygame.draw.rect(tela, BOTAO_BORDA, rect, width=2, border_radius=10)
    desenhar_texto(tela, texto, fonte, TEXTO_CLARO, rect.center)
    return hover


# ---------------------------------------------------------------------------
# As telas do jogo (menu, pausa, placar e derrota)
# ---------------------------------------------------------------------------
#
# Para os botoes, separamos duas coisas:
# - uma funcao "posicoes_botoes_..." que so calcula ONDE cada botao fica;
# - a funcao "desenhar_..." que DESENHA usando essas posicoes.
# Assim o loop principal pode descobrir onde o jogador clicou sem precisar
# redesenhar a tela, e o codigo fica mais facil de entender.

def posicoes_botoes_menu():
    """Devolve um dicionario {nome_do_botao: area na tela} do menu.

    As chaves sao os nomes dos niveis ('facil', 'medio'...) mais 'sair'.
    """
    largura_btn, altura_btn = 180, 50
    cx = LARGURA_TELA // 2
    x_esq = cx - 100
    x_dir = cx + 100

    centros = {
        "facil":   (x_esq, 250),
        "medio":   (x_dir, 250),
        "dificil": (x_esq, 330),
        "extremo": (x_dir, 330),
        "sair":    (cx, 420),
    }

    rects = {}
    for nome, (px, py) in centros.items():
        rect = pygame.Rect(0, 0, largura_btn, altura_btn)
        rect.center = (px, py)
        rects[nome] = rect
    return rects


def desenhar_menu(tela, recordes, fonte_titulo, fonte_botao, fonte_hud, fonte_rec, mouse_pos):
    """Desenha o menu inicial: titulo, botoes de dificuldade e botao de sair.

    Tambem devolve as areas dos botoes (vindas de posicoes_botoes_menu),
    caso o loop principal precise delas.
    """
    tela.fill(FUNDO)

    desenhar_texto(tela, "MemoryPy", fonte_titulo, AMARELO,
                   (LARGURA_TELA // 2, 100))
    desenhar_texto(tela, "Escolha a dificuldade", fonte_hud, CINZA,
                   (LARGURA_TELA // 2, 150))

    rects = posicoes_botoes_menu()

    # Desenha um botao para cada nivel, com o recorde daquele nivel embaixo.
    for nivel in NIVEIS:
        rect = rects[nivel]
        cfg = NIVEIS[nivel]
        _desenhar_botao(tela, f"{cfg['rotulo']} ({cfg['tempo']}s)", fonte_botao, rect, mouse_pos)
        rec = recordes.get(nivel, 0)
        desenhar_texto(tela, f"Recorde: {rec}", fonte_rec, CINZA,
                       (rect.centerx, rect.centery + 36))

    _desenhar_botao(tela, "Sair", fonte_botao, rects["sair"], mouse_pos)

    desenhar_texto(tela, "Durante o jogo:  P pausa   R reinicia   ESC sai",
                   fonte_hud, CINZA, (LARGURA_TELA // 2, 505))

    return rects


def posicoes_botoes_pausa():
    """Devolve {nome_do_botao: area} dos botoes da tela de pausa.

    As chaves sao 'retomar', 'menu' e 'sair'.
    """
    largura_btn, altura_btn = 220, 55
    cx = LARGURA_TELA // 2

    centros = {
        "retomar": (cx, ALTURA_TELA // 2 - 20),
        "menu":    (cx, ALTURA_TELA // 2 + 60),
        "sair":    (cx, ALTURA_TELA // 2 + 140),
    }

    rects = {}
    for nome, centro in centros.items():
        rect = pygame.Rect(0, 0, largura_btn, altura_btn)
        rect.center = centro
        rects[nome] = rect
    return rects


def desenhar_pausa(tela, fonte_titulo, fonte_botao, fonte_hud, mouse_pos):
    """Desenha a tela de pausa com os botoes Retomar, Menu e Sair.

    Tambem devolve as areas dos botoes (vindas de posicoes_botoes_pausa).
    """
    _overlay(tela, alpha=200)

    desenhar_texto(tela, "Pausado", fonte_titulo, AMARELO,
                   (LARGURA_TELA // 2, ALTURA_TELA // 2 - 120))

    rects = posicoes_botoes_pausa()
    _desenhar_botao(tela, "Retomar (P)", fonte_botao, rects["retomar"], mouse_pos)
    _desenhar_botao(tela, "Menu", fonte_botao, rects["menu"], mouse_pos)
    _desenhar_botao(tela, "Sair", fonte_botao, rects["sair"], mouse_pos)

    return rects


def desenhar_placar(tela, estado, recorde, fonte_hud):
    """Mostra na faixa de cima as informacoes da partida: tentativas,
    pontos, tempo restante, recorde do nivel e os atalhos de teclado."""
    desenhar_texto(tela, f"Tentativas: {estado['tentativas']}", fonte_hud, TEXTO_CLARO, (120, 30))
    desenhar_texto(tela, f"Pontos: {estado['pontos']}", fonte_hud, TEXTO_CLARO, (340, 30))
    desenhar_texto(tela, f"Tempo: {tempo_restante(estado)}s", fonte_hud, TEXTO_CLARO, (520, 30))
    desenhar_texto(tela, f"Recorde: {recorde}", fonte_hud, TEXTO_CLARO, (690, 30))

    rotulo = NIVEIS[estado["nivel"]]["rotulo"]
    desenhar_texto(tela, f"Nivel: {rotulo}    P: pausar    R: reiniciar    ESC: sair",
                   fonte_hud, CINZA, (LARGURA_TELA // 2, 70))


def desenhar_fim(tela, estado, fonte_fim):
    """Desenha a tela de derrota (quando o tempo acaba).
    A tela de vitoria fica no arquivo tela_vitoria.py."""
    _overlay(tela)
    desenhar_texto(tela, "Tempo esgotado!", fonte_fim, CARTA_ENCONTRADA,
                   (LARGURA_TELA // 2, ALTURA_TELA // 2 - 20))
    desenhar_texto(tela, "R: jogar de novo    M: menu", fonte_fim, TEXTO_CLARO,
                   (LARGURA_TELA // 2, ALTURA_TELA // 2 + 40))


# ---------------------------------------------------------------------------
# O motor do jogo (loop principal)
# ---------------------------------------------------------------------------

def executar_jogo():
    """Prepara tudo e roda o jogo do inicio ao fim.

    Esta funcao faz o "loop principal": enquanto o jogo estiver aberto, ela
    repete tres passos a cada quadro -> (1) ler o que o jogador fez (mouse e
    teclado), (2) atualizar o estado da partida e (3) desenhar a tela.
    """
    pygame.init()
    tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
    pygame.display.set_caption(TITULO_JOGO)
    relogio = pygame.time.Clock()

    # Cria as fontes uma unica vez (e mais rapido do que criar a cada quadro).
    fonte_hud    = pygame.font.SysFont("arial", 22)
    fonte_fim    = pygame.font.SysFont("arial", 40, bold=True)
    fonte_titulo = pygame.font.SysFont("arial", 64, bold=True)
    fonte_botao  = pygame.font.SysFont("arial", 24, bold=True)
    fonte_rec    = pygame.font.SysFont("arial", 16)

    # Carrega os recordes salvos e prepara o estado inicial (no menu).
    recordes = carregar_recordes(CAMINHO_RECORDE)
    estado = estado_inicial(NIVEL_PADRAO)
    fonte_carta = _fonte_carta(estado["tamanho_carta"])

    rodando = True
    while rodando:
        relogio.tick(FPS)                  # segura o jogo na velocidade certa
        mouse_pos = pygame.mouse.get_pos()
        situacao = estado["situacao"]      # em que tela/momento o jogo esta

        # --- Passo 1: ler o que o jogador fez (teclado e mouse) ---
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

            # Teclas: ESC (pausa/sai), P (pausa), R (reinicia), M (menu).
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
                    estado = estado_inicial(NIVEL_PADRAO)   # volta para o menu

            # Clique do mouse: o efeito depende da tela em que estamos.
            elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:

                if situacao == "menu":
                    # Descobre em qual botao do menu o jogador clicou.
                    rects = posicoes_botoes_menu()
                    for nivel in NIVEIS:
                        if rects[nivel].collidepoint(mouse_pos):
                            estado, fonte_carta = iniciar_partida(nivel)
                            break
                    if rects["sair"].collidepoint(mouse_pos):
                        rodando = False

                elif situacao == "pausado":
                    # Descobre qual botao da pausa o jogador clicou.
                    rects = posicoes_botoes_pausa()
                    if rects["retomar"].collidepoint(mouse_pos):
                        retomar(estado)
                    elif rects["menu"].collidepoint(mouse_pos):
                        estado = estado_inicial(NIVEL_PADRAO)
                    elif rects["sair"].collidepoint(mouse_pos):
                        rodando = False

                elif situacao == "jogando":
                    tratar_clique(estado, mouse_pos)

        # --- Passo 2: atualizar a partida (so quando esta jogando) ---
        if situacao == "jogando":
            avaliar_jogada(estado)   # confere se as duas cartas formam par
            atualizar_erro(estado)   # esconde de novo as cartas erradas

            # Se o tempo zerou e ainda nao venceu, o jogador perde.
            if tempo_restante(estado) <= 0:
                estado["situacao"] = "derrota"

            # Se a jogada acima resultou em vitoria, calcula o bonus de tempo
            # e, se for o caso, guarda o novo recorde do nivel.
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

        # --- Passo 3: desenhar a tela conforme o momento do jogo ---
        if situacao == "menu":
            desenhar_menu(tela, recordes, fonte_titulo, fonte_botao, fonte_hud, fonte_rec, mouse_pos)

        else:
            # Desenha o tabuleiro e o placar (vale para jogando/pausa/fim).
            tela.fill(FUNDO)
            for carta in estado["tabuleiro"]:
                desenhar_carta(tela, carta, fonte_carta)
            recorde_nivel = recordes.get(estado["nivel"], 0)
            desenhar_placar(tela, estado, recorde_nivel, fonte_hud)

            # Por cima do tabuleiro, mostra a tela extra conforme a situacao.
            if situacao == "pausado":
                desenhar_pausa(tela, fonte_titulo, fonte_botao, fonte_hud, mouse_pos)
            elif situacao == "vitoria":
                desenhar_tela_vitoria(tela, estado, recorde_nivel, estado["novo_recorde"], estado["tempo_vitoria"])
            elif situacao == "derrota":
                desenhar_fim(tela, estado, fonte_fim)

        # Mostra na tela tudo o que foi desenhado neste quadro.
        pygame.display.flip()

    # Saiu do loop: fecha a janela e encerra o pygame.
    pygame.quit()