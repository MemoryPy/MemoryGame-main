"""Gera os efeitos sonoros e a música de fundo do jogo.

Este script cria arquivos .wav simples (tons sintetizados por código, sem
usar nenhum som ou música de terceiros) e salva em assets/sons/. Ele só
precisa ser executado de novo se algum som for alterado: os arquivos .wav
gerados já ficam salvos no repositório, então o jogo não precisa rodar
este script para funcionar.

Para gerar (ou regenerar) os sons:
    python -m scripts.gerar_sons
"""

import math
import os
import struct
import wave

TAXA_AMOSTRAGEM = 44100
PASTA_SONS = os.path.join(os.path.dirname(__file__), "..", "assets", "sons")


def _nota(frequencia, duracao_s, volume=0.5):
    """Gera as amostras (em -1.0 a 1.0) de uma nota senoidal com um
    envelope simples de ataque/decaimento, para o som não "estalar"
    no começo e no fim.
    """
    total_amostras = int(TAXA_AMOSTRAGEM * duracao_s)
    amostras = []
    ataque = max(1, int(total_amostras * 0.1))
    decaimento = max(1, int(total_amostras * 0.3))

    for i in range(total_amostras):
        onda = math.sin(2 * math.pi * frequencia * (i / TAXA_AMOSTRAGEM))

        if i < ataque:
            envelope = i / ataque
        elif i > total_amostras - decaimento:
            envelope = (total_amostras - i) / decaimento
        else:
            envelope = 1.0

        amostras.append(onda * envelope * volume)

    return amostras


def _salvar_wav(caminho, amostras):
    """Grava uma lista de amostras (-1.0 a 1.0) como um .wav mono de 16 bits."""
    with wave.open(caminho, "w") as arquivo:
        arquivo.setnchannels(1)
        arquivo.setsampwidth(2)
        arquivo.setframerate(TAXA_AMOSTRAGEM)

        # Cada amostra (-1.0 a 1.0) precisa virar um numero inteiro de 16
        # bits antes de ir para o arquivo. Por isso convertemos uma por uma
        # e vamos juntando tudo num unico bloco de bytes.
        quadros = b""
        for amostra in amostras:
            amostra_limitada = max(-1.0, min(1.0, amostra))
            inteiro = int(amostra_limitada * 32767)
            quadros += struct.pack("<h", inteiro)
        arquivo.writeframes(quadros)


def gerar_efeito_acerto():
    """Som curto e ascendente, tocado quando o jogador encontra um par."""
    return _nota(660, 0.09, volume=0.5) + _nota(880, 0.12, volume=0.5)


def gerar_efeito_erro():
    """Som curto e descendente, tocado quando as duas cartas não combinam."""
    return _nota(320, 0.08, volume=0.4) + _nota(220, 0.12, volume=0.4)


def gerar_efeito_vitoria():
    """Pequeno arpejo ascendente, tocado na tela de vitória."""
    notas = [523, 659, 784, 1046]
    amostras = []
    for nota in notas:
        amostras += _nota(nota, 0.14, volume=0.45)
    return amostras


def gerar_musica_fundo():
    """Um loop curto e suave, tocado em segundo plano durante a partida."""
    sequencia = [392, 440, 523, 440, 392, 330, 392, 440]
    amostras = []
    for nota in sequencia:
        amostras += _nota(nota, 0.5, volume=0.18)
    return amostras


def gerar_todos_os_sons():
    """Gera e salva todos os arquivos de som do jogo em assets/sons/."""
    os.makedirs(PASTA_SONS, exist_ok=True)

    sons = {
        "acerto.wav": gerar_efeito_acerto(),
        "erro.wav": gerar_efeito_erro(),
        "vitoria.wav": gerar_efeito_vitoria(),
        "musica_fundo.wav": gerar_musica_fundo(),
    }

    for nome_arquivo, amostras in sons.items():
        _salvar_wav(os.path.join(PASTA_SONS, nome_arquivo), amostras)
        print(f"Gerado: assets/sons/{nome_arquivo}")


if __name__ == "__main__":
    gerar_todos_os_sons()
