# Dados

Esta pasta guarda os arquivos que o jogo precisa manter salvos entre uma
partida e outra.

## Arquivos

- `record.json`: guarda os dados pessoais do jogador, em quatro partes:
  - `recordes`: melhor pontuacao de cada nivel de dificuldade;
  - `estatisticas`: melhor tempo, menor numero de tentativas e total de
    partidas jogadas em cada nivel;
  - `ranking`: os melhores nomes e pontuacoes de cada nivel (top 5);
  - `conquistas`: quais conquistas o jogador ja desbloqueou;
  - `preferencias`: tema (claro/escuro) e se o som esta ligado.

  Ele e criado automaticamente conforme o jogador joga, e nao vai para o
  repositorio (esta no `.gitignore`), porque esses dados sao pessoais de
  cada maquina.

## Observacao

Evite versionar dados pessoais reais dos jogadores.
