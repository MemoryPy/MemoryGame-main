# Sons

Pasta para efeitos sonoros e trilhas do jogo.

## Conteudo atual

- `acerto.wav`, `erro.wav`, `vitoria.wav`: efeitos curtos tocados ao formar
  um par, errar um par e vencer a partida.
- `musica_fundo.wav`: trilha simples tocada em loop durante a partida.

Todos esses arquivos sao gerados por codigo (tons sinteticos, sem nenhum
som de terceiros) pelo script `scripts/gerar_sons.py`. Para gerar de novo
(por exemplo, apos mudar algum som no script):

```bash
python -m scripts.gerar_sons
```

## Recomendações

- Use formatos leves, como `.ogg` para musica e `.wav` para efeitos curtos.
- Normalize volume para evitar diferencas bruscas entre arquivos.
- Documente a origem dos audios quando forem externos.
