# MemoryPy

**MemoryPy** é um **Jogo da Memória** desenvolvido em **Python** com a biblioteca **Pygame**, como projeto final da disciplina de **Introdução a Algoritmos / Programação** (PUC Minas — CDIA).

O jogador escolhe uma dificuldade no menu, vira cartas em uma grade e precisa encontrar todos os pares iguais antes que o tempo da partida acabe. O projeto foi construído a partir do template oficial da disciplina, com foco em código organizado, modular e coerente com os conteúdos estudados.

## Integrantes do grupo

- Mario
- Guilherme
- Matheus
- Rafael

## Sobre o jogo

Ao abrir, o jogo mostra um **menu** onde o jogador escolhe a dificuldade. Em seguida aparece o tabuleiro com as cartas viradas para baixo. A cada turno, o jogador clica em **duas cartas** para revelá-las:

- Se as duas cartas forem **iguais**, elas permanecem abertas (ficam verdes) e o jogador soma pontos.
- Se forem **diferentes**, voltam a ficar ocultas após uma breve pausa (~0,7 s), exigindo que o jogador memorize as posições.

O desafio é completar o tabuleiro **antes do tempo acabar**, usando a memória para reduzir o número de tentativas.

### Níveis de dificuldade

O jogador escolhe entre quatro níveis no menu. Cada nível tem grade, tempo e peso de pontuação próprios, e guarda o **recorde separadamente**:

| Nível | Grade | Pares | Tempo | Peso (pontos) |
|-------|-------|-------|-------|----------------|
| Fácil | 4×4 | 8 | 90 s | 1× |
| Médio | 4×4 | 8 | 60 s | 1× |
| Difícil | 4×6 | 12 | 60 s | 2× |
| Extremo | 6×6 | 18 | 45 s | 3× |

### Como o jogador interage

| Ação | Comando |
|------|---------|
| Selecionar / revelar uma carta | **Clique esquerdo do mouse** |
| Escolher dificuldade / botões | **Clique esquerdo do mouse** |
| Pausar / retomar a partida | Tecla **P** |
| Reiniciar a partida | Tecla **R** |
| Voltar ao menu (na pausa ou no fim) | Tecla **M** |
| Pausar (em jogo) ou sair (nas outras telas) | Tecla **ESC** |

### Objetivo

Encontrar todos os pares de cartas iguais no menor número de tentativas possível, concluindo o tabuleiro antes que o cronômetro chegue a zero.

### Regras

- O tabuleiro é embaralhado a cada partida, com o tamanho definido pela dificuldade.
- O jogador revela **duas cartas por turno**.
- **Par igual:** as cartas ficam abertas e somam pontos (10 × peso do nível).
- **Par diferente:** as cartas voltam a ficar ocultas após a pausa.
- A partida tem **tempo limitado**, que varia conforme o nível.
- Ao vencer, sobra de tempo vira **pontos de bônus** (2 × peso por segundo restante).

### Condições de vitória e derrota

- **Vitória:** todos os pares são encontrados antes do tempo acabar. Aparece a tela "Você venceu!" com os pontos, o tempo e o recorde — e um aviso de **novo recorde**, se for o caso.
- **Derrota:** o tempo da partida se esgota antes de completar o tabuleiro. Aparece a tela "Tempo esgotado!".
- Em ambos os casos, o jogador pode pressionar **R** para jogar de novo ou **M** para voltar ao menu.

### O que aparece na tela

Na faixa superior (placar) são exibidos, em tempo real:

- **Tentativas** (quantas jogadas de duas cartas já foram feitas)
- **Pontos** da partida atual
- **Tempo** restante (em segundos)
- **Recorde** do nível
- O nível atual e os atalhos de teclado (P / R / ESC)

O título da janela é **"MemoryPy"**.

## Como executar o projeto

### 1. Clonar o repositório

```bash
git clone https://github.com/MemoryPy/MemoryGame-main.git
cd MemoryGame-main
```

### 2. Criar um ambiente virtual (recomendado)

Isola as dependências do projeto e evita conflitos com o Python do sistema.

```bash
python -m venv .venv

# Ativar no Linux/macOS:
source .venv/bin/activate

# Ativar no Windows (PowerShell):
.venv\Scripts\Activate.ps1
```

### 3. Instalar as dependências

```bash
pip install -r requirements.txt
```

### 4. Executar o jogo

```bash
python main.py
```

## Como executar os testes

Os testes cobrem a lógica do jogo (sem precisar abrir a janela):

```bash
python -m pytest
```

Saída esperada: todos os testes passando (atualmente **10 testes**).

## Observações de execução

- Em alguns sistemas (Linux/macOS), use `python3` e `pip3` no lugar de `python` e `pip`.
- No Linux com sessão **Wayland**, se aparecer o erro `pygame.error: windows not available`, rode o jogo assim: `SDL_VIDEODRIVER=x11 python main.py`.

## Estrutura do projeto

```
MemoryGame-main/
├── main.py              # Ponto de entrada: inicia o jogo
├── requirements.txt     # Dependências (pygame, pytest)
├── README.md            # Este arquivo
├── .gitignore           # Arquivos ignorados pelo Git
├── src/                 # Código-fonte do jogo
│   ├── __init__.py      # Torna 'src' um pacote Python
│   ├── jogo.py          # Loop principal, eventos, telas (menu, pausa, derrota)
│   ├── config.py        # Configurações: tela, cores, níveis, tempo, caminhos
│   ├── funcoes.py       # Lógica do jogo (funções puras, testáveis)
│   ├── sprites.py       # Desenho das cartas e dos textos
│   ├── tela_vitoria.py  # Tela de comemoração exibida ao vencer
│   └── dados.py         # Leitura e escrita dos recordes
├── assets/              # Imagens, fontes e sons (não usados no momento)
├── data/                # Arquivos persistentes
│   └── record.json      # Recordes por nível (gerado ao vencer; ignorado pelo Git)
├── tests/               # Testes automatizados (pytest)
│   └── test_logica.py   # Testes das funções de lógica
└── docs/                # Documentação
    └── proposta.MD      # Proposta inicial (Semana 1)
```

## Organização do código

O projeto é dividido em módulos com responsabilidades claras:

- **`main.py`** — ponto de entrada; apenas chama `executar_jogo()`.
- **`src/config.py`** — todas as constantes em um só lugar: tamanho da janela, cores, níveis de dificuldade, tempo de partida, pontos e o caminho do recorde.
- **`src/funcoes.py`** — a **lógica pura** do jogo, em funções independentes do Pygame (por isso são fáceis de testar): embaralhar as cartas, converter índice em coordenada, comparar um par, calcular pontos, calcular o bônus de tempo, verificar fim de jogo e checar novo recorde.
- **`src/sprites.py`** — a parte visual das cartas: desenha cada carta conforme o estado (oculta, aberta ou encontrada) e escreve textos na tela.
- **`src/tela_vitoria.py`** — a tela de comemoração mostrada quando o jogador vence.
- **`src/dados.py`** — persistência: lê e grava os recordes em JSON.
- **`src/jogo.py`** — o **loop principal**: trata eventos (mouse e teclado), controla os turnos de duas cartas, o temporizador, a pausa, as telas (menu, jogo, pausa, vitória e derrota) e a renderização.

## Conceitos da disciplina aplicados

| Conceito | Onde aparece no projeto |
|----------|--------------------------|
| Variáveis e entrada/saída | Estado da partida e leitura de cliques/teclas |
| Estruturas condicionais | Comparação de pares, fim de jogo, vitória/derrota |
| Laços de repetição | Loop principal do jogo e montagem do tabuleiro |
| Listas | Lista de cartas do tabuleiro |
| Dicionários | Cada carta e o recorde salvo em JSON |
| Tuplas | Coordenada `(linha, coluna)` de cada carta |
| Conjuntos | Pares já encontrados |
| Funções e modularização | Código dividido em módulos com funções específicas |
| Leitura e escrita de arquivos | Recorde em `data/record.json` |
| Testes automatizados | `tests/test_logica.py` com pytest |

### Estruturas de dados utilizadas

- **Lista** — `tabuleiro`, a sequência das cartas da partida.
- **Dicionário** — cada carta é um dicionário (`valor`, `posicao`, `rect`, `revelada`, `encontrada`); o estado da partida e os recordes por nível também são dicionários.
- **Tupla** — a posição de cada carta na grade, no formato `(linha, coluna)`.
- **Conjunto** — `pares_encontrados`, registrando os símbolos já combinados sem repetição.

### Leitura e escrita de arquivos

Os recordes são salvos em `data/record.json`, com um valor por nível de dificuldade:

```json
{
  "recordes": {
    "facil": 80,
    "extremo": 260
  }
}
```

Ao abrir o jogo, os recordes são carregados; ao vencer uma partida com pontuação maior que a salva naquele nível, o arquivo é atualizado. Se o arquivo não existir ainda, o jogo começa sem recordes (cada um vale 0).

## Uso do template da disciplina

O projeto foi desenvolvido **a partir do template oficial** ([IntroAlgs_pygame_template](https://github.com/ICEI-PUC-Minas-PPL-CDIA/IntroAlgs_pygame_template)), mantendo a estrutura de pastas e os arquivos base. O grupo **adaptou e reescreveu** o conteúdo dos módulos de `src/` para implementar a mecânica do jogo da memória, preservando a organização original do repositório.

## Assets externos

O jogo **não utiliza recursos externos** (imagens, sons ou fontes de terceiros): as cartas são desenhadas com formas geométricas do próprio Pygame e os textos usam a fonte padrão do sistema. Caso sejam adicionados assets livres futuramente, eles serão listados abaixo com origem e licença, conforme as regras de autoria do trabalho.

| Recurso | Tipo | Fonte / Autor | Licença |
|---------|------|---------------|---------|
| _(nenhum no momento)_ | | | |

## Principais desafios

- Implementar a **pausa entre cartas erradas** sem travar o loop do jogo (resolvido controlando o tempo por marcação de instante, não com `sleep`).
- Fazer o **cronômetro continuar certo após a pausa**, descontando o tempo parado.
- Sincronizar a **lógica de turnos** (duas cartas por jogada) com o **temporizador** da partida.
- Montar a grade de forma que **cartas e fonte se ajustem** ao tamanho de cada nível.
- Organizar a **persistência dos recordes por nível** e manter o código modular e testável.

## Status do desenvolvimento

- ✅ **Semana 1 — Proposta:** `docs/proposta.MD` com todos os itens pedidos.
- ✅ **Semana 2 — Protótipo:** janela Pygame, loop principal, grade 4×4, clique do mouse, lógica de pares, placar e código organizado em funções.
- ✅ **Semana 3 — Interações e regras:** menu de dificuldade, quatro níveis com grade dinâmica, pausa, bônus de tempo, telas de vitória/derrota, recordes por nível em arquivo e testes automatizados.

## Requisitos mínimos atendidos

- [x] Tela principal de jogo.
- [x] Controle de um elemento principal (seleção das cartas pelo mouse).
- [x] Mecânica central clara (combinar/completar os pares).
- [x] Indicador de desempenho (pontuação, tempo e recorde).
- [x] Condição clara de vitória e derrota.
- [x] Interação com elementos do jogo (as cartas).
- [x] Exibição de informações na tela e no título da janela.
- [x] Código organizado em funções.
- [x] Uso de estruturas de dados (lista, dicionário, tupla, conjunto).
- [x] Leitura e escrita em arquivo (`data/record.json`).
- [x] Documentação no `README.md`.
- [x] Proposta inicial em `docs/proposta.MD`.
- [x] Testes para as funções de lógica.

## Possíveis melhorias

Ideias planejadas para as próximas etapas (detalhadas na seção 17 da proposta): bônus de pontuação pelo tempo restante, tela de comemoração na vitória, menu inicial e pausa, sons e animações, níveis de dificuldade e ranking de jogadores.

## Observações para o grupo

- Manter o código organizado em módulos pequenos e com responsabilidade clara.
- Comentar as partes importantes da lógica, principalmente as regras do jogo.
- Registrar decisões técnicas neste README ao longo do desenvolvimento.
