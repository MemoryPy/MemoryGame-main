# Este arquivo cuida de salvar e ler o recorde em disco, para que a melhor
# pontuacao continue guardada mesmo depois de fechar o jogo. Os recordes
# ficam num arquivo JSON, separados por nivel de dificuldade.

import json


def carregar_recordes(caminho_arquivo):
    """Le os recordes salvos e devolve um dicionario {nivel: pontos}.

    Se o arquivo ainda nao existir (primeira vez que joga) ou estiver
    estragado, devolve um dicionario vazio em vez de quebrar o programa.
    """
    try:
        with open(caminho_arquivo, "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)
            recordes = dados.get("recordes", {})
            return {nivel: int(pontos) for nivel, pontos in recordes.items()}
    except (FileNotFoundError, ValueError, AttributeError, json.JSONDecodeError):
        return {}


def salvar_recordes(caminho_arquivo, recordes):
    """Grava no arquivo o dicionario de recordes de cada nivel."""
    dados = {"recordes": {nivel: int(pontos) for nivel, pontos in recordes.items()}}
    with open(caminho_arquivo, "w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, ensure_ascii=False, indent=2)
