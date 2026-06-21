# Aqui ficam as funcoes que desenham as cartas e os textos na tela.
# A parte visual do jogo fica separada da parte de regras (funcoes.py)
# para deixar o codigo mais organizado.

import math

import pygame

from src.config import DURACAO_ANIMACAO_MS, ICONES_CARTAS


def _desenhar_icone(tela, forma, cor, centro, raio):
    """Desenha o icone (forma + cor) de uma carta, no lugar de uma letra.

    Cada simbolo do jogo tem uma forma e uma cor proprias (ver
    ICONES_CARTAS em config.py), para o jogador conseguir diferenciar as
    cartas so pelo desenho.
    """
    cx, cy = centro

    if forma == "circulo":
        pygame.draw.circle(tela, cor, (cx, cy), raio)

    elif forma == "quadrado":
        rect = pygame.Rect(0, 0, raio * 1.7, raio * 1.7)
        rect.center = centro
        pygame.draw.rect(tela, cor, rect, border_radius=4)

    elif forma == "triangulo":
        pontos = [
            (cx, cy - raio),
            (cx - raio, cy + raio * 0.8),
            (cx + raio, cy + raio * 0.8),
        ]
        pygame.draw.polygon(tela, cor, pontos)

    elif forma == "diamante":
        pontos = [(cx, cy - raio), (cx + raio, cy), (cx, cy + raio), (cx - raio, cy)]
        pygame.draw.polygon(tela, cor, pontos)

    elif forma == "estrela":
        pontos = []
        for i in range(10):
            angulo = math.pi / 2 + i * math.pi / 5
            r = raio if i % 2 == 0 else raio * 0.45
            pontos.append((cx + r * math.cos(angulo), cy - r * math.sin(angulo)))
        pygame.draw.polygon(tela, cor, pontos)

    elif forma == "hexagono":
        pontos = []
        for i in range(6):
            angulo = math.pi / 6 + i * math.pi / 3
            pontos.append((cx + raio * math.cos(angulo), cy + raio * math.sin(angulo)))
        pygame.draw.polygon(tela, cor, pontos)

    elif forma == "cruz":
        espessura = raio * 0.7
        vertical = pygame.Rect(0, 0, espessura, raio * 2)
        vertical.center = centro
        horizontal = pygame.Rect(0, 0, raio * 2, espessura)
        horizontal.center = centro
        pygame.draw.rect(tela, cor, vertical, border_radius=3)
        pygame.draw.rect(tela, cor, horizontal, border_radius=3)

    elif forma == "coracao":
        r = raio * 0.6
        pygame.draw.circle(tela, cor, (int(cx - r * 0.6), int(cy - r * 0.3)), int(r))
        pygame.draw.circle(tela, cor, (int(cx + r * 0.6), int(cy - r * 0.3)), int(r))
        pontos = [
            (cx - raio, cy - r * 0.1),
            (cx + raio, cy - r * 0.1),
            (cx, cy + raio),
        ]
        pygame.draw.polygon(tela, cor, pontos)

    elif forma == "pentagono":
        pontos = []
        for i in range(5):
            angulo = -math.pi / 2 + i * 2 * math.pi / 5
            pontos.append((cx + raio * math.cos(angulo), cy + raio * math.sin(angulo)))
        pygame.draw.polygon(tela, cor, pontos)


def _progresso_animacao(carta, agora):
    """Calcula o quanto (de 0.0 a 1.0) a animacao de virar a carta ja
    avancou, com base em quando ela foi revelada por ultimo.

    Se a carta nao tem animacao em andamento (ou ja terminou), devolve 1.0,
    ou seja, "totalmente virada", sem nenhum efeito.
    """
    inicio = carta.get("anim_inicio")
    if inicio is None:
        return 1.0
    decorrido = agora - inicio
    if decorrido >= DURACAO_ANIMACAO_MS:
        return 1.0
    return max(0.0, decorrido / DURACAO_ANIMACAO_MS)


def desenhar_carta(tela, carta, fonte, tema, agora=None):
    """Desenha uma carta, mudando a aparencia conforme o estado dela.

    Sao tres situacoes possiveis:
    - ja encontrada: fundo verde, icone (ou letra) e um brilho ao redor;
    - virada agora nesta jogada: fundo claro e mostra o icone (ou letra);
    - ainda escondida: fundo escuro e mostra um "?".

    Quando a carta acabou de virar (revelada ou encontrada), um pequeno
    efeito de "achatamento" simula a animacao de virar a carta.
    """
    rect = carta["rect"]

    if carta["encontrada"]:
        cor_fundo = tema["carta_encontrada"]
        mostrar_simbolo = True
    elif carta["revelada"]:
        cor_fundo = tema["carta_aberta"]
        mostrar_simbolo = True
    else:
        cor_fundo = tema["carta_oculta"]
        mostrar_simbolo = False

    # A animacao "encolhe" a largura da carta e depois volta ao tamanho
    # normal, simulando o efeito de virar (como uma carta de baralho).
    if agora is not None:
        progresso = _progresso_animacao(carta, agora)
    else:
        progresso = 1.0

    if progresso < 0.5:
        escala = abs(1.0 - 2.0 * progresso)
    else:
        escala = 2.0 * progresso - 1.0

    if carta.get("anim_inicio") is not None:
        escala = max(0.15, escala)
    else:
        escala = 1.0

    largura_animada = max(4, int(rect.width * escala))
    rect_animado = pygame.Rect(0, 0, largura_animada, rect.height)
    rect_animado.center = rect.center

    # Brilho ao redor da carta quando o par e encontrado: um contorno mais
    # claro e levemente maior, atras do retangulo principal da carta.
    if carta["encontrada"]:
        brilho = rect.inflate(8, 8)
        pygame.draw.rect(tela, tema["amarelo"], brilho, width=3, border_radius=14)

    pygame.draw.rect(tela, cor_fundo, rect_animado, border_radius=12)

    # So desenha o icone/letra quando a carta ja virou o suficiente (mais
    # da metade da animacao), para parecer que o desenho "aparece" quando a
    # carta fica de frente para o jogador.
    if mostrar_simbolo and escala > 0.5:
        valor = carta["valor"]
        if valor in ICONES_CARTAS:
            forma, cor = ICONES_CARTAS[valor]
            raio = int(rect.width * 0.28)
            _desenhar_icone(tela, forma, cor, rect.center, raio)
        else:
            texto = fonte.render(valor, True, tema["texto_carta"])
            tela.blit(texto, texto.get_rect(center=rect.center))
    elif not mostrar_simbolo:
        texto = fonte.render("?", True, tema["texto_claro"])
        tela.blit(texto, texto.get_rect(center=rect.center))


def desenhar_texto(tela, texto, fonte, cor, centro):
    """Escreve um texto na tela, centralizado na posicao informada.

    Usada o tempo todo para mostrar placar, titulos e botoes, evitando
    repetir as mesmas linhas em varios lugares.
    """
    superficie = fonte.render(texto, True, cor)
    retangulo = superficie.get_rect(center=centro)
    tela.blit(superficie, retangulo)
