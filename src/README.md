# Código-fonte (`src`)

Esta pasta contém os módulos principais do jogo.

## Arquivos

- `jogo.py`: loop principal, eventos, turnos de duas cartas, temporizador, pausa, dica, combo, cartas especiais, modos de 1 e 2 jogadores e renderização.
- `config.py`: constantes globais (tela, cores, temas, níveis de dificuldade, ícones das cartas, cartas especiais, combo, dica e caminho dos dados salvos).
- `funcoes.py`: lógica do jogo em funções puras e testáveis (embaralhar, coordenadas, comparar par, pontuar, combo, precisão, estatísticas, conquistas e ranking).
- `sprites.py`: desenho das cartas (ícone, animação de virar e brilho ao formar par) e dos textos na tela.
- `tela_vitoria.py`: telas de comemoração ao vencer (1 jogador, com ranking/conquistas, e 2 jogadores).
- `dados.py`: leitura e gravação de recordes, estatísticas, ranking, conquistas e preferências em `data/record.json`.
- `audio.py`: efeitos sonoros e música de fundo pelo mixer do Pygame.

## Dica de evolução

Quando o projeto crescer, mantenha módulos pequenos e separados por responsabilidade.
