import json


def carregar_recordes(caminho_arquivo):
    """Carrega o dicionário de recordes por nível ({nivel: pontos}).

    Retorna um dicionário vazio se o arquivo não existir ou estiver inválido.
    """
    try:
        with open(caminho_arquivo, "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)
            recordes = dados.get("recordes", {})
            return {nivel: int(pontos) for nivel, pontos in recordes.items()}
    except (FileNotFoundError, ValueError, AttributeError, json.JSONDecodeError):
        return {}


def salvar_recordes(caminho_arquivo, recordes):
    """Salva o dicionário de recordes por nível em um arquivo JSON."""
    dados = {"recordes": {nivel: int(pontos) for nivel, pontos in recordes.items()}}
    with open(caminho_arquivo, "w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, ensure_ascii=False, indent=2)