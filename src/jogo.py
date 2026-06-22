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
    SIMBOLOS_ESPECIAIS,
    SIMBOLO_CURINGA,
    SIMBOLO_BONUS_TEMPO,
    SIMBOLO_EMBARALHA,
    SEGUNDOS_BONUS_CARTA,
    NIVEIS,
    NIVEL_PADRAO,
    CAMINHO_RECORDE,
    TAMANHO_RANKING,
    TAMANHO_MAXIMO_NOME,
    CUSTO_DICA,
    DICAS_MAXIMAS,
    DURACAO_DICA_MS,
    TEMAS,
    MARGEM_LATERAL,
    MARGEM_INFERIOR,
)
from src.funcoes import (
    montar_simbolos_do_nivel,
    criar_valores_embaralhados,
    indice_para_coordenada,
    verificar_par,
    calcular_pontos,
    calcular_bonus_tempo,
    todos_pares_encontrados,
    eh_novo_recorde,
    calcular_precisao,
    atualizar_combo,
    calcular_multiplicador_combo,
    atualizar_estatisticas,
    verificar_conquistas,
    qualifica_para_ranking,
    atualizar_ranking,
    completar_par_bonus,
    reembaralhar_ocultas,
)
from src.sprites import desenhar_carta, desenhar_texto
from src.dados import (
    carregar_recordes,
    salvar_recordes,
    carregar_estatisticas,
    salvar_estatisticas,
    carregar_ranking,
    salvar_ranking,
    carregar_conquistas,
    salvar_conquistas,
    carregar_preferencias,
    salvar_preferencias,
)
from src.tela_vitoria import desenhar_tela_vitoria, desenhar_tela_vitoria_2p
from src import audio


# ---------------------------------------------------------------------------
# Montagem do tabuleiro e do estado da partida
# ---------------------------------------------------------------------------

def criar_tabuleiro(linhas, colunas, cartas_especiais=False):
    """Monta as cartas de uma grade do tamanho pedido.

    Calcula o tamanho de carta que cabe na tela, embaralha os simbolos e
    cria cada carta ja com sua posicao. Se 'cartas_especiais' for True,
    alguns pares normais sao trocados por cartas com efeito especial
    (curinga, bonus de tempo e embaralha). Devolve a lista de cartas e o
    tamanho de carta usado (para a fonte combinar com o tamanho).
    """
    largura_disp = LARGURA_TELA - 2 * MARGEM_LATERAL
    altura_disp = ALTURA_TELA - ESPACO_TOPO - MARGEM_INFERIOR

    carta_por_largura = (largura_disp - (colunas - 1) * MARGEM) / colunas
    carta_por_altura = (altura_disp - (linhas - 1) * MARGEM) / linhas
    tamanho = int(min(carta_por_largura, carta_por_altura))

    largura_grade = colunas * tamanho + (colunas - 1) * MARGEM
    altura_grade = linhas * tamanho + (linhas - 1) * MARGEM
    inicio_x = (LARGURA_TELA - largura_grade) // 2
    inicio_y = ESPACO_TOPO + (altura_disp - altura_grade) // 2

    numero_pares = (linhas * colunas) // 2
    simbolos_do_nivel = montar_simbolos_do_nivel(
        SIMBOLOS, numero_pares, SIMBOLOS_ESPECIAIS, cartas_especiais
    )
    valores = criar_valores_embaralhados(simbolos_do_nivel)

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
            "anim_inicio": None,  # quando != None, a carta esta "virando"
        }
        tabuleiro.append(carta)

    return tabuleiro, tamanho


def estado_inicial(nivel=NIVEL_PADRAO, modo="1p", cartas_especiais=False):
    """Cria o "estado" da partida: um dicionario que guarda tudo que muda
    durante o jogo (cartas, pontos, tempo, situacao atual etc.).

    Manter tudo num so dicionario facilita reiniciar a partida: basta criar
    um estado novo. O jogo comeca na situacao "menu".
    """
    cfg = NIVEIS[nivel]
    tabuleiro, tamanho = criar_tabuleiro(cfg["linhas"], cfg["colunas"], cartas_especiais)

    return {
        "tabuleiro": tabuleiro,
        "tamanho_carta": tamanho,
        "nivel": nivel,
        "modo": modo,                  # "1p" ou "2p"
        "cartas_especiais": cartas_especiais,
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
        "ultimo_resultado": None,  # "acerto"/"erro" na última jogada (para o som)
        # --- combo e dica (só no modo 1 jogador) ---
        "combo": 0,
        "dicas_usadas": 0,
        "dica_expira": None,
        "dica_indices": [],
        "precisao": 0,
        "conquistas_novas": set(),
        "pedindo_nome": False,
        "entrada_nome": "",
        # --- modo 2 jogadores ---
        "jogador_atual": 1,
        "pontos_jogadores": [0, 0],
        "tentativas_jogadores": [0, 0],
    }


def _fonte_carta(tamanho):
    """Cria a fonte das letras das cartas, proporcional ao tamanho da carta
    (cartas menores, no nivel extremo, usam letras menores)."""
    return pygame.font.SysFont("arial", max(20, int(tamanho * 0.55)), bold=True)


def iniciar_partida(nivel, modo="1p", cartas_especiais=False):
    """Comeca de fato uma partida no nivel escolhido.

    Cria um estado novo, marca a situacao como "jogando" e zera o relogio.
    Devolve tambem a fonte das cartas, que depende do tamanho da grade.
    """
    estado = estado_inicial(nivel, modo, cartas_especiais)
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

    Ignora o clique se ja existem duas cartas viradas (esperando comparacao),
    se uma dica esta sendo mostrada ou se a carta clicada ja esta aberta.
    """
    if estado["erro_em"] is not None or estado["dica_expira"] is not None:
        return
    if len(estado["selecionadas"]) >= 2:
        return

    for indice, carta in enumerate(estado["tabuleiro"]):
        if carta["rect"].collidepoint(posicao_mouse):
            if carta["revelada"] or carta["encontrada"]:
                return
            carta["revelada"] = True
            carta["anim_inicio"] = pygame.time.get_ticks()
            estado["selecionadas"].append(indice)
            break


def _aplicar_efeito_especial(estado, valor):
    """Aplica o efeito de uma carta especial quando o par dela e encontrado.

    - Curinga: completa automaticamente outro par que ainda esta oculto.
    - Bonus de tempo: soma alguns segundos ao tempo da partida.
    - Embaralha: sorteia uma nova posicao para os valores ainda ocultos.
    """
    if valor == SIMBOLO_CURINGA:
        # Monta a lista dos valores que ainda estao ocultos (sem contar as
        # proprias cartas especiais), para sortear um par para completar.
        ocultos = []
        for carta in estado["tabuleiro"]:
            if not carta["encontrada"] and carta["valor"] not in SIMBOLOS_ESPECIAIS:
                ocultos.append(carta["valor"])

        alvo = completar_par_bonus(ocultos)
        if alvo is not None:
            completados = 0
            for carta in estado["tabuleiro"]:
                if completados >= 2:
                    break
                if not carta["encontrada"] and carta["valor"] == alvo:
                    carta["encontrada"] = True
                    carta["revelada"] = True
                    completados += 1
            estado["pares_encontrados"].add(alvo)

    elif valor == SIMBOLO_BONUS_TEMPO:
        estado["tempo_limite"] += SEGUNDOS_BONUS_CARTA

    elif valor == SIMBOLO_EMBARALHA:
        # Junta os indices e os valores de todas as cartas ainda ocultas,
        # sorteia uma ordem nova para os valores e devolve cada um para o
        # tabuleiro, na mesma posicao da lista (por isso os indices e os
        # valores embaralhados precisam estar alinhados).
        indices_ocultos = []
        valores_ocultos = []
        for indice, carta in enumerate(estado["tabuleiro"]):
            if not carta["encontrada"] and not carta["revelada"]:
                indices_ocultos.append(indice)
                valores_ocultos.append(carta["valor"])

        novos_valores = reembaralhar_ocultas(valores_ocultos)
        for posicao in range(len(indices_ocultos)):
            indice = indices_ocultos[posicao]
            estado["tabuleiro"][indice]["valor"] = novos_valores[posicao]


def avaliar_jogada(estado):
    """Compara as duas cartas viradas e decide o que acontece.

    Se forem iguais, viram um par (somam pontos e ficam abertas) e, se foi
    o ultimo par, a partida e vencida. Se forem diferentes, marca o momento
    para depois esconde-las de novo. No modo 2 jogadores, tambem cuida da
    pontuacao de cada jogador e da troca de turno.
    """
    estado["ultimo_resultado"] = None
    if len(estado["selecionadas"]) != 2 or estado["erro_em"] is not None:
        return

    estado["tentativas"] += 1
    if estado["modo"] == "2p":
        estado["tentativas_jogadores"][estado["jogador_atual"] - 1] += 1

    indice_a, indice_b = estado["selecionadas"]
    carta_a = estado["tabuleiro"][indice_a]
    carta_b = estado["tabuleiro"][indice_b]

    if verificar_par(carta_a["valor"], carta_b["valor"]):
        valor_par = carta_a["valor"]
        carta_a["encontrada"] = True
        carta_b["encontrada"] = True
        estado["pares_encontrados"].add(valor_par)
        estado["selecionadas"] = []
        estado["ultimo_resultado"] = "acerto"

        pontos_par = PONTOS_POR_PAR * estado["peso"]

        if estado["modo"] == "1p":
            estado["combo"] = atualizar_combo(estado["combo"], acertou=True)
            multiplicador = calcular_multiplicador_combo(estado["combo"])
            pontos_par = int(pontos_par * multiplicador)
            estado["pontos"] = calcular_pontos(estado["pontos"], pontos_par)
            _aplicar_efeito_especial(estado, valor_par)
        else:
            jogador = estado["jogador_atual"]
            estado["pontos_jogadores"][jogador - 1] += pontos_par
            _aplicar_efeito_especial(estado, valor_par)

        if todos_pares_encontrados(estado["pares_encontrados"], estado["numero_pares"]):
            estado["situacao"] = "vitoria"
            estado["tempo_vitoria"] = tempo_restante(estado)
    else:
        estado["erro_em"] = pygame.time.get_ticks()
        estado["ultimo_resultado"] = "erro"

        if estado["modo"] == "1p":
            estado["combo"] = atualizar_combo(estado["combo"], acertou=False)
        else:
            estado["jogador_atual"] = 3 - estado["jogador_atual"]


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


def usar_dica(estado):
    """Revela rapidamente um par ainda oculto, custando alguns pontos.

    Só funciona no modo 1 jogador, enquanto não há cartas viradas esperando
    comparação e enquanto ainda houver dicas disponíveis nesta partida.
    """
    if estado["modo"] != "1p":
        return
    if estado["dicas_usadas"] >= DICAS_MAXIMAS:
        return
    if len(estado["selecionadas"]) > 0 or estado["erro_em"] is not None or estado["dica_expira"] is not None:
        return

    indices_ocultos = []
    valores_ocultos = []
    for indice, carta in enumerate(estado["tabuleiro"]):
        if not carta["encontrada"] and not carta["revelada"]:
            indices_ocultos.append(indice)
            valores_ocultos.append(carta["valor"])

    alvo = completar_par_bonus(valores_ocultos)
    if alvo is None:
        return

    # Procura, entre as cartas ocultas, as duas que tem o valor sorteado.
    indices_da_dica = []
    for indice in indices_ocultos:
        if len(indices_da_dica) >= 2:
            break
        if estado["tabuleiro"][indice]["valor"] == alvo:
            indices_da_dica.append(indice)

    agora = pygame.time.get_ticks()
    for indice in indices_da_dica:
        estado["tabuleiro"][indice]["revelada"] = True
        estado["tabuleiro"][indice]["anim_inicio"] = agora

    estado["dicas_usadas"] += 1
    estado["pontos"] = max(0, estado["pontos"] - CUSTO_DICA)
    estado["dica_expira"] = agora + DURACAO_DICA_MS
    estado["dica_indices"] = indices_da_dica


def atualizar_dica(estado):
    """Esconde de novo as cartas reveladas pela dica, quando o tempo dela acaba."""
    if estado["dica_expira"] is None:
        return
    if pygame.time.get_ticks() >= estado["dica_expira"]:
        for indice in estado["dica_indices"]:
            if not estado["tabuleiro"][indice]["encontrada"]:
                estado["tabuleiro"][indice]["revelada"] = False
        estado["dica_expira"] = None
        estado["dica_indices"] = []


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


def _desenhar_botao(tela, texto, fonte, rect, mouse_pos, tema):
    """Desenha um botao na tela e muda a cor quando o mouse passa por cima.

    Devolve True se o mouse estiver em cima do botao, o que ajuda a saber
    se ele foi clicado.
    """
    hover = rect.collidepoint(mouse_pos)
    if hover:
        cor_fundo = tema["botao_hover"]
    else:
        cor_fundo = tema["botao_fundo"]
    pygame.draw.rect(tela, cor_fundo, rect, border_radius=10)
    pygame.draw.rect(tela, tema["botao_borda"], rect, width=2, border_radius=10)
    desenhar_texto(tela, texto, fonte, tema["texto_claro"], rect.center)
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
        "facil":   (x_esq, 230),
        "medio":   (x_dir, 230),
        "dificil": (x_esq, 300),
        "extremo": (x_dir, 300),
        "modo":      (x_esq, 380),
        "especiais": (x_dir, 380),
        "sair":    (cx, 460),
    }

    rects = {}
    for nome, (px, py) in centros.items():
        rect = pygame.Rect(0, 0, largura_btn, altura_btn)
        rect.center = (px, py)
        rects[nome] = rect
    return rects


def desenhar_menu(tela, recordes, fonte_titulo, fonte_botao, fonte_hud, fonte_rec,
                   mouse_pos, tema, modo_selecionado, especiais_selecionado):
    """Desenha o menu inicial: titulo, botoes de dificuldade, opcoes de modo
    de jogo e cartas especiais, e botao de sair.

    Tambem devolve as areas dos botoes (vindas de posicoes_botoes_menu),
    caso o loop principal precise delas.
    """
    tela.fill(tema["fundo"])

    desenhar_texto(tela, "MemoryPy", fonte_titulo, tema["amarelo"],
                   (LARGURA_TELA // 2, 70))
    desenhar_texto(tela, "Escolha a dificuldade", fonte_hud, tema["cinza"],
                   (LARGURA_TELA // 2, 120))

    rects = posicoes_botoes_menu()

    for nivel in NIVEIS:
        rect = rects[nivel]
        cfg = NIVEIS[nivel]
        _desenhar_botao(tela, f"{cfg['rotulo']} ({cfg['tempo']}s)", fonte_botao, rect, mouse_pos, tema)
        rec = recordes.get(nivel, 0)
        desenhar_texto(tela, f"Recorde: {rec}", fonte_rec, tema["cinza"],
                       (rect.centerx, rect.centery + 36))

    if modo_selecionado == "1p":
        rotulo_modo = "Modo: 1 Jogador"
    else:
        rotulo_modo = "Modo: 2 Jogadores"
    _desenhar_botao(tela, rotulo_modo, fonte_botao, rects["modo"], mouse_pos, tema)

    if especiais_selecionado:
        rotulo_especiais = "Especiais: Ligadas"
    else:
        rotulo_especiais = "Especiais: Desligadas"
    _desenhar_botao(tela, rotulo_especiais, fonte_botao, rects["especiais"], mouse_pos, tema)

    _desenhar_botao(tela, "Sair", fonte_botao, rects["sair"], mouse_pos, tema)

    desenhar_texto(tela, "Durante o jogo:  P pausa   R reinicia   H dica   ESC sai",
                   fonte_hud, tema["cinza"], (LARGURA_TELA // 2, 525))
    desenhar_texto(tela, "T troca o tema   S liga/desliga o som",
                   fonte_hud, tema["cinza"], (LARGURA_TELA // 2, 550))

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


def desenhar_pausa(tela, fonte_titulo, fonte_botao, fonte_hud, mouse_pos, tema):
    """Desenha a tela de pausa com os botoes Retomar, Menu e Sair.

    Tambem devolve as areas dos botoes (vindas de posicoes_botoes_pausa).
    """
    _overlay(tela, alpha=200)

    desenhar_texto(tela, "Pausado", fonte_titulo, tema["amarelo"],
                   (LARGURA_TELA // 2, ALTURA_TELA // 2 - 120))

    rects = posicoes_botoes_pausa()
    _desenhar_botao(tela, "Retomar (P)", fonte_botao, rects["retomar"], mouse_pos, tema)
    _desenhar_botao(tela, "Menu", fonte_botao, rects["menu"], mouse_pos, tema)
    _desenhar_botao(tela, "Sair", fonte_botao, rects["sair"], mouse_pos, tema)

    return rects


def desenhar_placar(tela, estado, recorde, fonte_hud, tema):
    """Mostra na faixa de cima as informacoes da partida: tentativas,
    pontos, tempo restante, recorde do nivel, combo e dicas (modo 1 jogador)."""
    desenhar_texto(tela, f"Tentativas: {estado['tentativas']}", fonte_hud, tema["texto_claro"], (110, 30))
    desenhar_texto(tela, f"Pontos: {estado['pontos']}", fonte_hud, tema["texto_claro"], (310, 30))
    desenhar_texto(tela, f"Tempo: {tempo_restante(estado)}s", fonte_hud, tema["texto_claro"], (490, 30))
    desenhar_texto(tela, f"Recorde: {recorde}", fonte_hud, tema["texto_claro"], (650, 30))

    rotulo = NIVEIS[estado["nivel"]]["rotulo"]
    multiplicador = calcular_multiplicador_combo(estado["combo"])
    dicas_restantes = DICAS_MAXIMAS - estado["dicas_usadas"]
    extra = f"Combo: x{multiplicador:.1f}    Dicas: {dicas_restantes}/{DICAS_MAXIMAS}"
    desenhar_texto(tela, f"Nivel: {rotulo}    {extra}",
                   fonte_hud, tema["cinza"], (LARGURA_TELA // 2, 70))


def desenhar_placar_2p(tela, estado, fonte_hud, tema):
    """Mostra o placar do modo 2 jogadores: pontos de cada jogador, de
    quem é a vez e o tempo restante da partida."""
    if estado["jogador_atual"] == 1:
        cor_p1 = tema["amarelo"]
        cor_p2 = tema["texto_claro"]
        vez = "Vez do Jogador 1"
    else:
        cor_p1 = tema["texto_claro"]
        cor_p2 = tema["amarelo"]
        vez = "Vez do Jogador 2"

    desenhar_texto(tela, f"Jogador 1: {estado['pontos_jogadores'][0]} pts", fonte_hud, cor_p1, (160, 30))
    desenhar_texto(tela, f"Jogador 2: {estado['pontos_jogadores'][1]} pts", fonte_hud, cor_p2, (640, 30))
    desenhar_texto(tela, f"Tempo: {tempo_restante(estado)}s", fonte_hud, tema["texto_claro"], (400, 30))

    desenhar_texto(tela, vez, fonte_hud, tema["cinza"], (LARGURA_TELA // 2, 70))


def desenhar_fim(tela, estado, fonte_fim, tema):
    """Desenha a tela de derrota (quando o tempo acaba).
    A tela de vitoria fica no arquivo tela_vitoria.py."""
    _overlay(tela)
    desenhar_texto(tela, "Tempo esgotado!", fonte_fim, tema["carta_encontrada"],
                   (LARGURA_TELA // 2, ALTURA_TELA // 2 - 20))
    desenhar_texto(tela, "R: jogar de novo    M: menu", fonte_fim, tema["texto_claro"],
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

    audio.inicializar()

    fonte_hud    = pygame.font.SysFont("arial", 20)
    fonte_fim    = pygame.font.SysFont("arial", 40, bold=True)
    fonte_titulo = pygame.font.SysFont("arial", 56, bold=True)
    fonte_botao  = pygame.font.SysFont("arial", 22, bold=True)
    fonte_rec    = pygame.font.SysFont("arial", 16)

    # Carrega os dados salvos (recordes, estatisticas, ranking, conquistas e
    # preferencias) e prepara o estado inicial (no menu).
    recordes = carregar_recordes(CAMINHO_RECORDE)
    estatisticas = carregar_estatisticas(CAMINHO_RECORDE)
    ranking = carregar_ranking(CAMINHO_RECORDE)
    conquistas = carregar_conquistas(CAMINHO_RECORDE)
    preferencias = carregar_preferencias(CAMINHO_RECORDE)

    modo_selecionado = "1p"
    especiais_selecionado = False

    estado = estado_inicial(NIVEL_PADRAO)
    fonte_carta = _fonte_carta(estado["tamanho_carta"])

    rodando = True
    while rodando:
        relogio.tick(FPS)
        mouse_pos = pygame.mouse.get_pos()
        situacao = estado["situacao"]
        tema = TEMAS[preferencias["tema"]]

        # --- Passo 1: ler o que o jogador fez (teclado e mouse) ---
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

            elif evento.type == pygame.KEYDOWN:

                # Enquanto o jogo pede o nome para o ranking, as teclas
                # servem só para digitar (letras, apagar e confirmar).
                if estado.get("pedindo_nome"):
                    if evento.key == pygame.K_RETURN:
                        nome = estado["entrada_nome"].strip() or "Jogador"
                        nivel = estado["nivel"]
                        ranking[nivel] = atualizar_ranking(
                            ranking.get(nivel, []), nome, estado["pontos"], TAMANHO_RANKING
                        )
                        salvar_ranking(CAMINHO_RECORDE, ranking)
                        estado["pedindo_nome"] = False
                    elif evento.key == pygame.K_BACKSPACE:
                        estado["entrada_nome"] = estado["entrada_nome"][:-1]
                    elif evento.unicode and evento.unicode.isprintable():
                        if len(estado["entrada_nome"]) < TAMANHO_MAXIMO_NOME:
                            estado["entrada_nome"] += evento.unicode
                    continue

                if evento.key == pygame.K_ESCAPE:
                    if situacao == "jogando":
                        pausar(estado)
                    else:
                        rodando = False

                elif evento.key == pygame.K_p and situacao == "jogando":
                    pausar(estado)

                elif evento.key == pygame.K_p and situacao == "pausado":
                    retomar(estado)

                elif evento.key == pygame.K_h and situacao == "jogando":
                    usar_dica(estado)

                elif evento.key == pygame.K_t:
                    temas = list(TEMAS.keys())
                    idx = temas.index(preferencias["tema"])
                    preferencias["tema"] = temas[(idx + 1) % len(temas)]
                    salvar_preferencias(CAMINHO_RECORDE, preferencias)

                elif evento.key == pygame.K_s:
                    preferencias["som_ativado"] = not preferencias["som_ativado"]
                    salvar_preferencias(CAMINHO_RECORDE, preferencias)
                    if not preferencias["som_ativado"]:
                        audio.parar_musica_fundo()

                elif evento.key == pygame.K_r and situacao in ("jogando", "vitoria", "derrota"):
                    estado, fonte_carta = iniciar_partida(
                        estado["nivel"], estado["modo"], estado["cartas_especiais"]
                    )

                elif evento.key == pygame.K_m and situacao in ("vitoria", "derrota", "pausado"):
                    estado = estado_inicial(NIVEL_PADRAO)
                    audio.parar_musica_fundo()

            elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:

                if situacao == "menu":
                    rects = posicoes_botoes_menu()
                    for nivel in NIVEIS:
                        if rects[nivel].collidepoint(mouse_pos):
                            estado, fonte_carta = iniciar_partida(
                                nivel, modo_selecionado, especiais_selecionado
                            )
                            break
                    if rects["modo"].collidepoint(mouse_pos):
                        if modo_selecionado == "1p":
                            modo_selecionado = "2p"
                        else:
                            modo_selecionado = "1p"
                    if rects["especiais"].collidepoint(mouse_pos):
                        especiais_selecionado = not especiais_selecionado
                    if rects["sair"].collidepoint(mouse_pos):
                        rodando = False

                elif situacao == "pausado":
                    rects = posicoes_botoes_pausa()
                    if rects["retomar"].collidepoint(mouse_pos):
                        retomar(estado)
                    elif rects["menu"].collidepoint(mouse_pos):
                        estado = estado_inicial(NIVEL_PADRAO)
                        audio.parar_musica_fundo()
                    elif rects["sair"].collidepoint(mouse_pos):
                        rodando = False

                elif situacao == "jogando":
                    tratar_clique(estado, mouse_pos)

        # --- Passo 2: atualizar a partida (so quando esta jogando) ---
        if situacao == "jogando":
            audio.tocar_musica_fundo(preferencias["som_ativado"])

            avaliar_jogada(estado)
            atualizar_erro(estado)
            atualizar_dica(estado)

            if estado["ultimo_resultado"] == "acerto":
                audio.tocar_efeito("acerto", preferencias["som_ativado"])
            elif estado["ultimo_resultado"] == "erro":
                audio.tocar_efeito("erro", preferencias["som_ativado"])

            if tempo_restante(estado) <= 0 and estado["situacao"] == "jogando":
                estado["situacao"] = "derrota"

            # Quando a partida termina (vitoria ou derrota), o bloco abaixo
            # roda só nesse exato quadro: "situacao" foi lida antes da
            # jogada acima, então o "if situacao == jogando" continua valido
            # mesmo que avaliar_jogada/tempo tenha acabado de mudar o estado.
            if estado["situacao"] == "vitoria":
                audio.tocar_efeito("vitoria", preferencias["som_ativado"])
                audio.parar_musica_fundo()

                if estado["modo"] == "1p":
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

                    estado["precisao"] = calcular_precisao(
                        estado["tentativas"], len(estado["pares_encontrados"])
                    )

                    stats_nivel = atualizar_estatisticas(
                        estatisticas.get(nivel, {}), venceu=True,
                        tentativas=estado["tentativas"], tempo_restante=estado["tempo_vitoria"],
                    )
                    estatisticas[nivel] = stats_nivel
                    salvar_estatisticas(CAMINHO_RECORDE, estatisticas)

                    resumo = {
                        "tentativas": estado["tentativas"],
                        "numero_pares": estado["numero_pares"],
                        "tempo_restante": estado["tempo_vitoria"],
                        "tempo_limite": estado["tempo_limite"],
                        "nivel": nivel,
                        "dicas_usadas": estado["dicas_usadas"],
                        "total_partidas": stats_nivel["partidas"],
                    }
                    novas = verificar_conquistas(resumo, conquistas)
                    estado["conquistas_novas"] = novas
                    if novas:
                        conquistas |= novas
                        salvar_conquistas(CAMINHO_RECORDE, conquistas)

                    ranking_nivel = ranking.get(nivel, [])
                    if qualifica_para_ranking(ranking_nivel, estado["pontos"], TAMANHO_RANKING):
                        estado["pedindo_nome"] = True

            elif estado["situacao"] == "derrota":
                audio.parar_musica_fundo()
                if estado["modo"] == "1p":
                    nivel = estado["nivel"]
                    estatisticas[nivel] = atualizar_estatisticas(
                        estatisticas.get(nivel, {}), venceu=False,
                        tentativas=estado["tentativas"], tempo_restante=0,
                    )
                    salvar_estatisticas(CAMINHO_RECORDE, estatisticas)

        # --- Passo 3: desenhar a tela conforme o momento do jogo ---
        if situacao == "menu":
            desenhar_menu(tela, recordes, fonte_titulo, fonte_botao, fonte_hud, fonte_rec,
                          mouse_pos, tema, modo_selecionado, especiais_selecionado)

        else:
            agora = pygame.time.get_ticks()
            tela.fill(tema["fundo"])
            for carta in estado["tabuleiro"]:
                desenhar_carta(tela, carta, fonte_carta, tema, agora)

            if estado["modo"] == "2p":
                desenhar_placar_2p(tela, estado, fonte_hud, tema)
            else:
                recorde_nivel = recordes.get(estado["nivel"], 0)
                desenhar_placar(tela, estado, recorde_nivel, fonte_hud, tema)

            if situacao == "pausado":
                desenhar_pausa(tela, fonte_titulo, fonte_botao, fonte_hud, mouse_pos, tema)
            elif situacao == "vitoria":
                if estado["modo"] == "2p":
                    desenhar_tela_vitoria_2p(tela, estado)
                else:
                    nivel = estado["nivel"]
                    desenhar_tela_vitoria(
                        tela, estado, recordes.get(nivel, 0), estado["novo_recorde"],
                        estado["tempo_vitoria"], estatisticas.get(nivel, {}),
                        estado["conquistas_novas"], ranking.get(nivel, []),
                        estado["entrada_nome"], estado["pedindo_nome"],
                    )
            elif situacao == "derrota":
                desenhar_fim(tela, estado, fonte_fim, tema)

        pygame.display.flip()

    pygame.quit()