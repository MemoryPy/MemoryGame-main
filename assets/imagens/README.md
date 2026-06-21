# Imagens

Pasta destinada a sprites, fundos, icones e outros elementos visuais.

## Conteudo atual

- `spritesheet.bmp`: spritesheet base do template. Nao e usada nas cartas
  do jogo (os icones das cartas sao formas desenhadas em codigo, ver
  `src/sprites.py`), porque os sprites dela (personagens e inimigos de um
  jogo top-down) nao combinam com os simbolos que o jogo precisa.

## Recomendações

- Separe imagens por tema quando o projeto crescer.
- Mantenha dimensoes e padroes consistentes para facilitar colisao e animacao.
- Prefira formatos com transparencia quando necessario (ex.: `.png`).
