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

# Caminho do arquivo onde ficam salvos os recordes de cada nivel.
CAMINHO_RECORDE = "data/record.json"