# Este arquivo cuida de salvar e ler os dados persistentes do jogador num
# unico arquivo JSON: o recorde de cada nivel, as estatisticas pessoais, o
# ranking com nomes e as conquistas desbloqueadas. Cada um tem sua propria
# chave dentro do arquivo, para nao misturar os formatos.

import json


def _carregar_tudo(caminho_arquivo):
    """Le o arquivo de dados completo e devolve um dicionario com as quatro
    secoes (recordes, estatisticas, ranking, conquistas).

    Se o arquivo ainda nao existir ou estiver estragado, devolve as quatro
    secoes vazias em vez de quebrar o programa.
    """
    try:
        with open(caminho_arquivo, "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)
    except (FileNotFoundError, ValueError, AttributeError, json.JSONDecodeError):
        dados = {}

    return {
        "recordes": dados.get("recordes", {}) or {},
        "estatisticas": dados.get("estatisticas", {}) or {},
        "ranking": dados.get("ranking", {}) or {},
        "conquistas": dados.get("conquistas", []) or [],
        "preferencias": dados.get("preferencias", {}) or {},
    }


def _salvar_tudo(caminho_arquivo, dados):
    """Grava no arquivo as quatro secoes de dados, formatadas em JSON."""
    with open(caminho_arquivo, "w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, ensure_ascii=False, indent=2)


def carregar_recordes(caminho_arquivo):
    """Le os recordes salvos e devolve um dicionario {nivel: pontos}."""
    recordes = _carregar_tudo(caminho_arquivo)["recordes"]
    return {nivel: int(pontos) for nivel, pontos in recordes.items()}


def salvar_recordes(caminho_arquivo, recordes):
    """Grava o dicionario de recordes de cada nivel, sem afetar as outras secoes."""
    dados = _carregar_tudo(caminho_arquivo)
    dados["recordes"] = {nivel: int(pontos) for nivel, pontos in recordes.items()}
    _salvar_tudo(caminho_arquivo, dados)


def carregar_estatisticas(caminho_arquivo):
    """Le as estatisticas pessoais salvas: {nivel: {partidas, vitorias,
    menor_tentativas, melhor_tempo}}."""
    return _carregar_tudo(caminho_arquivo)["estatisticas"]


def salvar_estatisticas(caminho_arquivo, estatisticas):
    """Grava as estatisticas pessoais de cada nivel, sem afetar as outras secoes."""
    dados = _carregar_tudo(caminho_arquivo)
    dados["estatisticas"] = estatisticas
    _salvar_tudo(caminho_arquivo, dados)


def carregar_ranking(caminho_arquivo):
    """Le o ranking salvo: {nivel: [{"nome": ..., "pontos": ...}, ...]}."""
    return _carregar_tudo(caminho_arquivo)["ranking"]


def salvar_ranking(caminho_arquivo, ranking):
    """Grava o ranking de cada nivel, sem afetar as outras secoes."""
    dados = _carregar_tudo(caminho_arquivo)
    dados["ranking"] = ranking
    _salvar_tudo(caminho_arquivo, dados)


def carregar_conquistas(caminho_arquivo):
    """Le as conquistas desbloqueadas e devolve um conjunto de strings."""
    return set(_carregar_tudo(caminho_arquivo)["conquistas"])


def salvar_conquistas(caminho_arquivo, conquistas):
    """Grava o conjunto de conquistas desbloqueadas, sem afetar as outras secoes."""
    dados = _carregar_tudo(caminho_arquivo)
    dados["conquistas"] = sorted(conquistas)
    _salvar_tudo(caminho_arquivo, dados)


def carregar_preferencias(caminho_arquivo):
    """Le as preferencias do jogador (tema e som), com valores padrao caso
    ainda nao tenham sido salvas."""
    padrao = {"tema": "escuro", "som_ativado": True}
    padrao.update(_carregar_tudo(caminho_arquivo)["preferencias"])
    return padrao


def salvar_preferencias(caminho_arquivo, preferencias):
    """Grava as preferencias do jogador, sem afetar as outras secoes."""
    dados = _carregar_tudo(caminho_arquivo)
    dados["preferencias"] = preferencias
    _salvar_tudo(caminho_arquivo, dados)
