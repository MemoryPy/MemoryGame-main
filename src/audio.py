# Este arquivo cuida dos efeitos sonoros e da musica de fundo. Os arquivos
# .wav usados aqui sao gerados por codigo (veja scripts/gerar_sons.py), sem
# nenhum som de terceiros.
#
# Em alguns computadores (ou em testes automatizados) pode nao existir uma
# placa de som disponivel. Por isso, todas as funcoes daqui sao "seguras":
# se o som nao puder ser inicializado, o jogo continua funcionando normal,
# soh sem tocar nada.

import os

import pygame

_PASTA_SONS = os.path.join(os.path.dirname(__file__), "..", "assets", "sons")

_disponivel = False
_efeitos = {}


def inicializar():
    """Liga o sistema de som do Pygame e carrega os efeitos sonoros.

    Devolve True se conseguiu inicializar o som, ou False se nao for
    possivel (por exemplo, sem placa de som). Nesse caso, as outras funcoes
    deste arquivo simplesmente nao fazem nada.
    """
    global _disponivel, _efeitos

    try:
        pygame.mixer.init()
        _efeitos = {
            "acerto": pygame.mixer.Sound(os.path.join(_PASTA_SONS, "acerto.wav")),
            "erro": pygame.mixer.Sound(os.path.join(_PASTA_SONS, "erro.wav")),
            "vitoria": pygame.mixer.Sound(os.path.join(_PASTA_SONS, "vitoria.wav")),
        }
        _disponivel = True
    except (pygame.error, FileNotFoundError):
        _disponivel = False

    return _disponivel


def tocar_efeito(nome, som_ativado=True):
    """Toca um efeito sonoro ('acerto', 'erro' ou 'vitoria'), se o som
    estiver disponivel e ativado."""
    if _disponivel and som_ativado and nome in _efeitos:
        _efeitos[nome].play()


def tocar_musica_fundo(som_ativado=True):
    """Comeca a tocar a musica de fundo em loop, se o som estiver disponivel
    e ativado. Se a musica ja estiver tocando, nao faz nada."""
    if not (_disponivel and som_ativado):
        return
    if pygame.mixer.music.get_busy():
        return
    try:
        pygame.mixer.music.load(os.path.join(_PASTA_SONS, "musica_fundo.wav"))
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(loops=-1)
    except (pygame.error, FileNotFoundError):
        pass


def parar_musica_fundo():
    """Para a musica de fundo, se o som estiver disponivel."""
    if _disponivel:
        pygame.mixer.music.stop()


def disponivel():
    """Diz se o sistema de som foi inicializado com sucesso."""
    return _disponivel
