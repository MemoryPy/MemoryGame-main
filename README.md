# MemoryPy

**MemoryPy** — Jogo da Memória. Projeto da disciplina de Introdução a Algoritmos / Programação (PUC Minas — CDIA), desenvolvido com Python e Pygame.

O jogador vira cartas em uma grade 4×4 e tenta encontrar todos os pares iguais antes que o tempo acabe.

## Integrantes do grupo

- Mario
- Guilherme
- Arthur Rodrigues
- Rafael

## Descrição do jogo

Na tela é exibida uma grade de **4×4 cartas (16 cartas, 8 pares)**, todas viradas para baixo. A cada turno, o jogador clica em duas cartas para revelá-las:

- Se as duas cartas forem **iguais**, elas permanecem abertas e o jogador pontua.
- Se forem **diferentes**, voltam a ficar ocultas após uma breve pausa.

O jogo desafia a memória do jogador: lembrar onde cada carta está reduz o número de tentativas e ajuda a concluir o tabuleiro dentro do tempo.

## Objetivo do jogador

Encontrar todos os 8 pares de cartas iguais antes que o tempo da partida se esgote, usando o menor número de tentativas possível.

## Regras do jogo

- O tabuleiro é uma grade 4×4 com 8 pares de cartas viradas para baixo.
- A cada turno, o jogador revela duas cartas com o mouse.
- Cartas iguais permanecem abertas e somam pontos.
- Cartas diferentes voltam a ficar ocultas após uma breve pausa.
- **Vitória:** todos os pares encontrados antes do tempo acabar.
- **Derrota:** o tempo da partida se esgota antes de completar o tabuleiro.

## Controles

- **Clique esquerdo do mouse:** selecionar/revelar uma carta.
- **R:** reiniciar a partida.
- **ESC:** sair do jogo.

## Estrutura do projeto

```
MemoryGame-main/
├── main.py              # Ponto de entrada da aplicação
├── requirements.txt     # Dependências do projeto
├── README.md            # Este arquivo
├── src/                 # Código-fonte principal do jogo
│   ├── jogo.py          # Loop principal e controle de estados
│   ├── config.py        # Configurações (tela, cores, tempo, caminhos)
│   ├── funcoes.py       # Funções auxiliares (embaralhar, comparar, pontuar)
│   ├── sprites.py       # Representação visual das cartas
│   └── dados.py         # Leitura e escrita do recorde
├── assets/              # Imagens, fontes e sons
├── data/                # Arquivos persistentes (recorde)
├── tests/               # Testes unitários com pytest
└── docs/                # Documentação do projeto (proposta inicial)
```

## Como executar o projeto

### 1. Clonar o repositório

```bash
git clone https://github.com/MemoryPy/GameMemory.git
cd GameMemory
```

### 2. Instalar as dependências

```bash
pip install -r requirements.txt
```

### 3. Executar o jogo

```bash
python main.py
```

## Como executar os testes

```bash
python -m pytest
```

## Conceitos da disciplina utilizados

- **Listas:** armazenam as cartas do tabuleiro.
- **Dicionários:** associam valores/símbolos às cartas e organizam o recorde salvo.
- **Tuplas:** representam as coordenadas `(linha, coluna)` de cada carta.
- **Conjuntos:** registram os pares já encontrados.
- **Estruturas de decisão e repetição:** controle de turnos, comparação de pares e loop principal do jogo.
- **Funções:** organização do código em blocos reutilizáveis.
- **Leitura e escrita de arquivos:** persistência do recorde.
- **Testes automatizados (pytest):** validação da lógica do jogo.

## Assets externos

Os recursos externos (imagens, fontes e sons) utilizados no projeto serão listados abaixo, com a devida indicação da fonte e licença.

| Recurso | Tipo | Fonte / Autor | Licença |
|---------|------|---------------|---------|
| _(a preencher)_ | | | |
| _(a preencher)_ | | | |

## Checklist mínimo para entrega

- [ ] README preenchido com nome final, descrição real, regras e controles do jogo.
- [ ] `docs/proposta.MD` atualizado com a proposta do grupo.
- [ ] Tabuleiro 4×4 com 8 pares embaralhados.
- [ ] Revelação de duas cartas por clique e comparação de pares.
- [ ] Sistema de pontuação e controle de tempo.
- [ ] Telas de vitória e derrota.
- [ ] Reinício com a tecla R e saída com ESC.
- [ ] Registro do recorde em arquivo.
- [ ] O jogo executa com `python main.py`.
- [ ] Os testes passam com `pytest`.

## Observações para o grupo

- Manter o código organizado em módulos pequenos e com responsabilidade clara.
- Comentar as partes importantes da lógica, principalmente as regras do jogo.
- Registrar decisões técnicas neste README ao longo do desenvolvimento.
