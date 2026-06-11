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
    ATRASO_ERRO,
    SIMBOLOS,
    FUNDO,
    TEXTO_CLARO,
    CARTA_ENCONTRADA,
    CINZA,
    CAMINHO_RECORDE,
)
from src.funcoes import (
    criar_valores_embaralhados,
    indice_para_coordenada,
    verificar_par,
    calcular_pontos,
    todos_pares_encontrados,
    eh_novo_recorde,
)
from src.sprites import desenhar_carta, desenhar_texto
from src.dados import carregar_recorde, salvar_recorde
from src.tela_vitoria import desenhar_tela_vitoria


def criar_tabuleiro():
    """Cria a lista de cartas do tabuleiro já posicionadas na tela.

    Cada carta é um dicionário com o seu símbolo, a coordenada (linha, coluna),
    o retângulo de desenho e os estados de revelada/encontrada.
    """
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
        "selecionadas": [],          # índices das cartas viradas nesta jogada
        "pares_encontrados": set(),  # conjunto de símbolos já combinados
        "tentativas": 0,
        "pontos": 0,
        "inicio": pygame.time.get_ticks(),
        "erro_em": None,             # momento em que duas cartas erradas viraram
        "situacao": "jogando",       # "jogando", "vitoria" ou "derrota"
        "tempo_vitoria": 0,          # segundos gastos até vencer
        "novo_recorde": False,       # True se esta partida bateu o recorde
    }


def tempo_restante(estado):
    """Calcula quantos segundos ainda restam na partida atual."""
    decorrido = (pygame.time.get_ticks() - estado["inicio"]) // 1000
    return max(0, TEMPO_LIMITE - decorrido)


def tratar_clique(estado, posicao_mouse):
    """Revela a carta clicada, respeitando as regras de turno."""
    # Ignora cliques enquanto aguardamos as cartas erradas voltarem.
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
            estado["tempo_vitoria"] = TEMPO_LIMITE - ((pygame.time.get_ticks() - estado["inicio"]) // 1000)
    else:
        # Marca o instante do erro para esconder as cartas após a pausa.
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


def desenhar_placar(tela, estado, recorde, fonte_hud):
    """Mostra tentativas, pontos, tempo e recorde no topo da tela."""
    desenhar_texto(
        tela, f"Tentativas: {estado['tentativas']}", fonte_hud, TEXTO_CLARO,
        (120, 30),
    )
    desenhar_texto(
        tela, f"Pontos: {estado['pontos']}", fonte_hud, TEXTO_CLARO,
        (340, 30),
    )
    desenhar_texto(
        tela, f"Tempo: {tempo_restante(estado)}s", fonte_hud, TEXTO_CLARO,
        (520, 30),
    )
    desenhar_texto(
        tela, f"Recorde: {recorde}", fonte_hud, TEXTO_CLARO,
        (690, 30),
    )
    desenhar_texto(
        tela, "R: reiniciar    ESC: sair", fonte_hud, CINZA,
        (LARGURA_TELA // 2, 70),
    )


def desenhar_fim(tela, estado, fonte_fim):
    """Desenha a mensagem de vitória ou derrota sobre o tabuleiro."""
    if estado["situacao"] == "vitoria":
        mensagem = "Voce venceu!"
    else:
        mensagem = "Tempo esgotado!"

    fundo = pygame.Surface((LARGURA_TELA, ALTURA_TELA))
    fundo.set_alpha(180)
    fundo.fill((0, 0, 0))
    tela.blit(fundo, (0, 0))

    desenhar_texto(
        tela, mensagem, fonte_fim, CARTA_ENCONTRADA,
        (LARGURA_TELA // 2, ALTURA_TELA // 2 - 20),
    )
    desenhar_texto(
        tela, "Pressione R para jogar de novo", fonte_fim, TEXTO_CLARO,
        (LARGURA_TELA // 2, ALTURA_TELA // 2 + 40),
    )


def executar_jogo():
    """Inicializa o Pygame e executa o loop principal do jogo da memória."""
    pygame.init()
    tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
    pygame.display.set_caption(TITULO_JOGO)
    relogio = pygame.time.Clock()

    fonte_carta = pygame.font.SysFont("arial", 48, bold=True)
    fonte_hud = pygame.font.SysFont("arial", 22)
    fonte_fim = pygame.font.SysFont("arial", 40, bold=True)

    recorde = carregar_recorde(CAMINHO_RECORDE)
    estado = estado_inicial()

    rodando = True
    while rodando:
        relogio.tick(FPS)

        # --- Eventos ---
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    rodando = False
                elif evento.key == pygame.K_r:
                    estado = estado_inicial()
            elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                if estado["situacao"] == "jogando":
                    tratar_clique(estado, evento.pos)

        # --- Atualização do estado ---
        if estado["situacao"] == "jogando":
            avaliar_jogada(estado)
            atualizar_erro(estado)

            if tempo_restante(estado) <= 0:
                estado["situacao"] = "derrota"

            if estado["situacao"] == "vitoria":
                if eh_novo_recorde(estado["pontos"], recorde):
                    recorde = estado["pontos"]
                    salvar_recorde(CAMINHO_RECORDE, recorde)
                    estado["novo_recorde"] = True

        # --- Renderização ---
        tela.fill(FUNDO)
        for carta in estado["tabuleiro"]:
            desenhar_carta(tela, carta, fonte_carta)
        desenhar_placar(tela, estado, recorde, fonte_hud)

        if estado["situacao"] == "vitoria":
            desenhar_tela_vitoria(
                tela, estado, recorde,
                estado["novo_recorde"],
                estado["tempo_vitoria"],
            )
        elif estado["situacao"] == "derrota":
            desenhar_fim(tela, estado, fonte_fim)

        pygame.display.flip()

    pygame.quit()
