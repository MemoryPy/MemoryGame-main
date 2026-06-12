# Configurações centrais do jogo (tela, cores, tabuleiro e caminhos de arquivos).

# Janela
LARGURA_TELA = 800
ALTURA_TELA = 600
FPS = 60
TITULO_JOGO = "MemoryPy"

# Tabuleiro 4x4 (8 pares)
LINHAS = 4
COLUNAS = 4
NUMERO_PARES = (LINHAS * COLUNAS) // 2

# Medidas das cartas (em pixels)
TAMANHO_CARTA = 110
MARGEM = 18
ESPACO_TOPO = 110  # área reservada no topo para o placar

# Tempo de partida (em segundos)
TEMPO_LIMITE = 60

# Regras de pontuação e ritmo
PONTOS_POR_PAR = 10
PONTOS_POR_SEGUNDO = 2  # bônus por segundo restante ao vencer
ATRASO_ERRO = 700  # tempo (ms) que duas cartas erradas ficam visíveis

# Cores (R, G, B)
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

# Símbolos usados nas cartas (um para cada par).
# Precisa ter pelo menos tantos quanto o maior número de pares (6x6 = 18).
SIMBOLOS = [
    "A", "B", "C", "D", "E", "F", "G", "H", "I",
    "J", "K", "L", "M", "N", "O", "P", "Q", "R",
]

# Níveis de dificuldade. Cada um define a grade (linhas x colunas), o tempo
# em segundos e o rótulo exibido nos botões/placar.
NIVEIS = {
    "facil":   {"linhas": 4, "colunas": 4, "tempo": 90, "rotulo": "Facil"},
    "medio":   {"linhas": 4, "colunas": 4, "tempo": 60, "rotulo": "Medio"},
    "dificil": {"linhas": 4, "colunas": 6, "tempo": 60, "rotulo": "Dificil"},
    "extremo": {"linhas": 6, "colunas": 6, "tempo": 45, "rotulo": "Extremo"},
}
NIVEL_PADRAO = "medio"

# Arquivo de recorde
CAMINHO_RECORDE = "data/record.json"