import json


def carregar_recorde(caminho_arquivo):
    """Carrega o recorde salvo em JSON; retorna 0 se o arquivo não existir
    ou estiver inválido."""
    try:
        with open(caminho_arquivo, "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)
            return int(dados.get("recorde", 0))
    except (FileNotFoundError, ValueError, json.JSONDecodeError):
        return 0


def salvar_recorde(caminho_arquivo, pontuacao):
    """Salva a pontuação recorde em um arquivo JSON estruturado."""
    dados = {"recorde": int(pontuacao)}
    with open(caminho_arquivo, "w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, ensure_ascii=False, indent=2)
