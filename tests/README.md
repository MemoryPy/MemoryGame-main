# Testes

Esta pasta contem testes automatizados do projeto.

## Arquivos

- `test_logica.py`: valida as funcoes puras de logica em `src/funcoes.py`
  (embaralhar, comparar par, pontuar, combo, precisao, conquistas, ranking)
  e a leitura/escrita dos dados em `src/dados.py` (recordes, estatisticas,
  ranking, conquistas e preferencias).

## Como executar

```bash
python -m pytest
```

## Boas praticas

- Crie testes para toda regra de pontuacao, vidas e condicoes de fim de jogo.
- Prefira funcoes pequenas e testaveis no modulo `src/funcoes.py`.
