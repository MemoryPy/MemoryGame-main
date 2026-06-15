# Arquivo principal: e ele que se roda para abrir o jogo (python main.py).
# So serve para chamar a funcao que liga o jogo de verdade, que esta em src/.

from src.jogo import executar_jogo


if __name__ == "__main__":
    # Esta linha so roda quando executamos este arquivo direto, e ai
    # iniciamos o jogo.
    executar_jogo()