# Código-fonte (`src`)

Esta pasta contém os módulos principais do jogo.

## Arquivos

- `jogo.py`: loop principal, eventos, turnos de duas cartas, temporizador, telas de vitória/derrota e renderização.
- `config.py`: constantes globais (tela, cores, grade 4×4, tempo, pontos e caminho do recorde).
- `funcoes.py`: lógica do jogo em funções puras e testáveis (embaralhar, coordenadas, comparar par, pontuar, fim de jogo, recorde).
- `sprites.py`: desenho das cartas (oculta/aberta/encontrada) e dos textos na tela.
- `dados.py`: leitura e gravação do recorde em `data/record.json`.

## Dica de evolução

Quando o projeto crescer, mantenha módulos pequenos e separados por responsabilidade.
