# Este arquivo guarda todos os "valores fixos" do jogo num lugar só.
# A ideia e poder mudar tamanho de tela, cores, tempo, pontos etc. aqui,
# sem precisar caçar esses numeros espalhados pelo resto do codigo.

# Tamanho da janela do jogo e quadros por segundo (velocidade da tela).
LARGURA_TELA = 800
ALTURA_TELA = 600
FPS = 60
TITULO_JOGO = "MemoryPy"

# Valores base do tabuleiro. Cada nivel de dificuldade (mais abaixo) pode
# usar uma grade diferente, mas estes servem de referencia padrao.
LINHAS = 4
COLUNAS = 4
NUMERO_PARES = (LINHAS * COLUNAS) // 2

# Medidas usadas para desenhar as cartas (em pixels).
TAMANHO_CARTA = 110
MARGEM = 18
ESPACO_TOPO = 110  # espaco reservado no topo da tela para o placar

# Quanto tempo dura uma partida, em segundos.
TEMPO_LIMITE = 60

# Regras de pontuação: quanto vale cada par e o bonus por terminar rapido.
PONTOS_POR_PAR = 10
PONTOS_POR_SEGUNDO = 2  # cada segundo que sobra ao vencer vira pontos extras
ATRASO_ERRO = 700  # tempo (em ms) que duas cartas erradas ficam viradas antes de esconder

# Cores do jogo, no formato (vermelho, verde, azul), cada um de 0 a 255.
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
CINZA = (212, 212, 212)
FUNDO = (28, 30, 46)
CARTA_OCULTA = (58, 64, 99)
CARTA_ABERTA = (240, 240, 245)
CARTA_ENCONTRADA = (120, 200, 140)
TEXTO_CLARO = (235, 235, 245)
TEXTO_CARTA = (40, 44, 70)
BOTAO_FUNDO = (58, 64, 99)
BOTAO_HOVER = (90, 100, 150)
BOTAO_BORDA = (120, 130, 180)
AMARELO = (255, 215, 80)

# Letras que aparecem nas cartas (cada letra forma um par).
# Como o nivel mais dificil tem 18 pares (grade 6x6), a lista precisa ter
# pelo menos 18 letras.
SIMBOLOS = [
    "A", "B", "C", "D", "E", "F", "G", "H", "I",
    "J", "K", "L", "M", "N", "O", "P", "Q", "R",
]

# Cartas especiais (ativadas por opcao no menu, funciona nos dois modos).
# Em vez de um par normal, alguns pares viram cartas com efeito extra.
SIMBOLO_CURINGA = "*"        # ao formar este par, completa outro par sozinho
SIMBOLO_BONUS_TEMPO = "+"    # ao formar este par, da segundos extras
SIMBOLO_EMBARALHA = "@"      # ao formar este par, reembaralha as cartas ocultas
SIMBOLOS_ESPECIAIS = [SIMBOLO_CURINGA, SIMBOLO_BONUS_TEMPO, SIMBOLO_EMBARALHA]
SEGUNDOS_BONUS_CARTA = 10    # segundos ganhos ao achar o par "bonus de tempo"

# Cada letra tambem tem um icone (forma + cor) desenhado na carta, no lugar
# da letra. As cores sao vibrantes, para o icone se destacar tanto no tema
# escuro quanto no tema claro. A combinacao forma+cor de cada letra e unica.
_VERMELHO_ICONE = (231, 76, 60)
_AZUL_ICONE = (52, 152, 219)
_VERDE_ICONE = (46, 204, 113)
_DOURADO_ICONE = (230, 180, 20)
_ROXO_ICONE = (155, 89, 182)
_LARANJA_ICONE = (230, 126, 34)
_TURQUESA_ICONE = (26, 188, 156)
_ROSA_ICONE = (236, 64, 122)
_CINZA_ICONE = (120, 130, 150)

_FORMAS_E_CORES = [
    ("circulo", _VERMELHO_ICONE),
    ("quadrado", _AZUL_ICONE),
    ("triangulo", _VERDE_ICONE),
    ("diamante", _DOURADO_ICONE),
    ("estrela", _ROXO_ICONE),
    ("hexagono", _LARANJA_ICONE),
    ("cruz", _TURQUESA_ICONE),
    ("coracao", _ROSA_ICONE),
    ("pentagono", _CINZA_ICONE),
    ("circulo", _AZUL_ICONE),
    ("quadrado", _VERDE_ICONE),
    ("triangulo", _DOURADO_ICONE),
    ("diamante", _ROXO_ICONE),
    ("estrela", _LARANJA_ICONE),
    ("hexagono", _TURQUESA_ICONE),
    ("cruz", _ROSA_ICONE),
    ("coracao", _CINZA_ICONE),
    ("pentagono", _VERMELHO_ICONE),
]

ICONES_CARTAS = {}
for _indice, _simbolo in enumerate(SIMBOLOS):
    ICONES_CARTAS[_simbolo] = _FORMAS_E_CORES[_indice]

# Icones das cartas especiais (cores diferentes para se destacarem das comuns).
ICONES_CARTAS[SIMBOLO_CURINGA] = ("estrela", _DOURADO_ICONE)
ICONES_CARTAS[SIMBOLO_BONUS_TEMPO] = ("cruz", _VERDE_ICONE)
ICONES_CARTAS[SIMBOLO_EMBARALHA] = ("hexagono", _ROXO_ICONE)

# Os quatro niveis de dificuldade do jogo. Para cada nivel guardamos:
# - linhas e colunas: o tamanho da grade de cartas;
# - tempo: quantos segundos o jogador tem;
# - peso: o multiplicador de pontos (quanto mais dificil, mais vale);
# - rotulo: o nome que aparece no botao e no placar.
NIVEIS = {
    "facil":   {"linhas": 4, "colunas": 4, "tempo": 90, "peso": 1, "rotulo": "Facil"},
    "medio":   {"linhas": 4, "colunas": 4, "tempo": 60, "peso": 1, "rotulo": "Medio"},
    "dificil": {"linhas": 4, "colunas": 6, "tempo": 60, "peso": 2, "rotulo": "Dificil"},
    "extremo": {"linhas": 6, "colunas": 6, "tempo": 45, "peso": 3, "rotulo": "Extremo"},
}
NIVEL_PADRAO = "medio"  # nivel que o jogo assume se nenhum for escolhido

# Caminho do arquivo onde ficam salvos os recordes, estatisticas, ranking e
# conquistas. E um unico arquivo JSON, com uma chave para cada coisa.
CAMINHO_RECORDE = "data/record.json"

# Quantos nomes entram no ranking (top N) de cada nivel.
TAMANHO_RANKING = 5

# Quantas letras o nome digitado no ranking pode ter, no maximo.
TAMANHO_MAXIMO_NOME = 12

# ---------------------------------------------------------------------------
# Combo: acertar pares em sequencia aumenta o multiplicador de pontos.
# ---------------------------------------------------------------------------
COMBO_INCREMENTO = 0.5   # quanto o multiplicador sobe a cada acerto seguido
COMBO_MAXIMO = 3.0       # multiplicador nao passa desse valor

# ---------------------------------------------------------------------------
# Dica: revela rapidamente um par escondido, custando pontos.
# ---------------------------------------------------------------------------
CUSTO_DICA = 5            # pontos descontados ao usar uma dica
DICAS_MAXIMAS = 3         # quantas dicas o jogador pode usar por partida
DURACAO_DICA_MS = 1000    # por quanto tempo a dica fica visivel (ms)

# ---------------------------------------------------------------------------
# Animacao das cartas (efeito de "virar" e brilho ao formar par).
# ---------------------------------------------------------------------------
DURACAO_ANIMACAO_MS = 220

# ---------------------------------------------------------------------------
# Temas visuais: o jogador pode trocar entre escuro (padrao) e claro.
# Cada tema e um dicionario com as mesmas chaves de cores usadas no jogo.
# ---------------------------------------------------------------------------
TEMA_ESCURO = {
    "fundo": FUNDO,
    "carta_oculta": CARTA_OCULTA,
    "carta_aberta": CARTA_ABERTA,
    "carta_encontrada": CARTA_ENCONTRADA,
    "texto_claro": TEXTO_CLARO,
    "texto_carta": TEXTO_CARTA,
    "cinza": CINZA,
    "botao_fundo": BOTAO_FUNDO,
    "botao_hover": BOTAO_HOVER,
    "botao_borda": BOTAO_BORDA,
    "amarelo": AMARELO,
}

TEMA_CLARO = {
    "fundo": (235, 237, 245),
    "carta_oculta": (190, 196, 215),
    "carta_aberta": (255, 255, 255),
    "carta_encontrada": (150, 215, 165),
    "texto_claro": (40, 44, 60),
    "texto_carta": (40, 44, 70),
    "cinza": (90, 95, 110),
    "botao_fundo": (210, 214, 230),
    "botao_hover": (180, 186, 210),
    "botao_borda": (140, 146, 170),
    "amarelo": (200, 120, 0),
}

TEMAS = {"escuro": TEMA_ESCURO, "claro": TEMA_CLARO}
TEMA_PADRAO = "escuro"

# Nome de exibicao de cada conquista (ver verificar_conquistas em funcoes.py).
CONQUISTAS_LABELS = {
    "perfeito": "Perfeito (venceu sem errar)",
    "sobrou_tempo": "Sobrou tempo (venceu com metade do tempo ou mais)",
    "sem_dica": "Sem ajuda (venceu sem usar dica)",
    "extremo_concluido": "Dominou o Extremo",
    "veterano": "Veterano (10 partidas jogadas)",
}