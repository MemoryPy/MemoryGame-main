# MemoryPy

**MemoryPy** é um **Jogo da Memória** desenvolvido em **Python** com a biblioteca **Pygame**, como projeto final da disciplina de **Introdução a Algoritmos / Programação** (PUC Minas — CDIA).

O jogador vira cartas em uma grade **4×4** e precisa encontrar todos os **8 pares** iguais antes que o tempo da partida acabe. O projeto foi construído a partir do template oficial da disciplina, com foco em código organizado, modular e coerente com os conteúdos estudados.

## Integrantes do grupo

- Mario
- Guilherme
- Matheus
- Rafael

## Sobre o jogo

Ao iniciar, a tela mostra uma grade de **4×4 (16 cartas, 8 pares)**, todas viradas para baixo. A cada turno, o jogador clica em **duas cartas** para revelá-las:

- Se as duas cartas forem **iguais**, elas permanecem abertas (ficam verdes) e o jogador soma pontos.
- Se forem **diferentes**, voltam a ficar ocultas após uma breve pausa (~0,7 s), exigindo que o jogador memorize as posições.

O desafio é completar o tabuleiro **antes do tempo acabar**, usando a memória para reduzir o número de tentativas.

### Como o jogador interage

| Ação | Comando |
|------|---------|
| Selecionar / revelar uma carta | **Clique esquerdo do mouse** |
| Reiniciar a partida | Tecla **R** |
| Sair do jogo | Tecla **ESC** (ou fechar a janela) |

### Objetivo

Encontrar os **8 pares** de cartas iguais no menor número de tentativas possível, concluindo o tabuleiro antes que o cronômetro chegue a zero.

### Regras

- O tabuleiro é uma grade **4×4** com 8 pares embaralhados a cada partida.
- O jogador revela **duas cartas por turno**.
- **Par igual:** as cartas ficam abertas e valem **+10 pontos**.
- **Par diferente:** as cartas voltam a ficar ocultas após a pausa.
- A partida tem **tempo limitado de 60 segundos**.

### Condições de vitória e derrota

- **Vitória:** todos os 8 pares são encontrados antes do tempo acabar. É exibida a tela "Você venceu!" e, se a pontuação superar o recorde, ele é atualizado no arquivo.
- **Derrota:** o tempo da partida se esgota antes de completar o tabuleiro. É exibida a tela "Tempo esgotado!".
- Em ambos os casos, o jogador pode pressionar **R** para jogar novamente.

### O que aparece na tela

Na faixa superior (placar) são exibidos, em tempo real:

- **Tentativas** (quantas jogadas de duas cartas já foram feitas)
- **Pontos** da partida atual
- **Tempo** restante (em segundos)
- **Recorde** salvo
- Lembrete dos controles (R / ESC)

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

Saída esperada: todos os testes passando (atualmente **9 testes**).

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
│   ├── jogo.py          # Loop principal, eventos, turnos, telas de fim
│   ├── config.py        # Configurações: tela, cores, grade, tempo, caminhos
│   ├── funcoes.py       # Lógica do jogo (funções puras, testáveis)
│   ├── sprites.py       # Desenho das cartas e dos textos
│   └── dados.py         # Leitura e escrita do recorde
├── assets/              # Imagens, fontes e sons (não usados no momento)
├── data/                # Arquivos persistentes
│   └── record.json      # Recorde salvo (gerado ao vencer uma partida)
├── tests/               # Testes automatizados (pytest)
│   └── test_logica.py   # Testes das funções de lógica
└── docs/                # Documentação
    └── proposta.MD      # Proposta inicial (Semana 1)
```

## Organização do código

O projeto é dividido em módulos com responsabilidades claras:

- **`main.py`** — ponto de entrada; apenas chama `executar_jogo()`.
- **`src/config.py`** — todas as constantes em um só lugar: tamanho da janela, cores, dimensões da grade 4×4, tempo de partida, pontos por par e o caminho do recorde.
- **`src/funcoes.py`** — a **lógica pura** do jogo, em funções independentes do Pygame (por isso são fáceis de testar): embaralhar as cartas, converter índice em coordenada, comparar um par, calcular pontos, verificar fim de jogo e checar novo recorde.
- **`src/sprites.py`** — a parte visual: desenha cada carta conforme o estado (oculta, aberta ou encontrada) e escreve textos na tela.
- **`src/dados.py`** — persistência: lê e grava o recorde em JSON.
- **`src/jogo.py`** — o **loop principal**: trata eventos (mouse e teclado), controla os turnos de duas cartas, o temporizador, as condições de vitória/derrota e a renderização.

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

- **Lista** — `tabuleiro`, a sequência das 16 cartas.
- **Dicionário** — cada carta é um dicionário (`valor`, `posicao`, `rect`, `revelada`, `encontrada`); o recorde também é um dicionário gravado em JSON.
- **Tupla** — a posição de cada carta na grade, no formato `(linha, coluna)`.
- **Conjunto** — `pares_encontrados`, registrando os símbolos já combinados sem repetição.

### Leitura e escrita de arquivos

O recorde é salvo em `data/record.json` no formato:

```json
{
  "recorde": 80
}
```

Ao abrir o jogo, o recorde é carregado; ao vencer uma partida com pontuação maior que a salva, o arquivo é atualizado. Se o arquivo não existir ainda, o jogo assume recorde 0.

## Uso do template da disciplina

O projeto foi desenvolvido **a partir do template oficial** ([IntroAlgs_pygame_template](https://github.com/ICEI-PUC-Minas-PPL-CDIA/IntroAlgs_pygame_template)), mantendo a estrutura de pastas e os arquivos base. O grupo **adaptou e reescreveu** o conteúdo dos módulos de `src/` para implementar a mecânica do jogo da memória, preservando a organização original do repositório.

## Assets externos

O jogo **não utiliza recursos externos** (imagens, sons ou fontes de terceiros): as cartas são desenhadas com formas geométricas do próprio Pygame e os textos usam a fonte padrão do sistema. Caso sejam adicionados assets livres futuramente, eles serão listados abaixo com origem e licença, conforme as regras de autoria do trabalho.

| Recurso | Tipo | Fonte / Autor | Licença |
|---------|------|---------------|---------|
| _(nenhum no momento)_ | | | |

## Principais desafios

- Implementar a **pausa entre cartas erradas** sem travar o loop do jogo (resolvido controlando o tempo por marcação de instante, não com `sleep`).
- Sincronizar a **lógica de turnos** (duas cartas por jogada) com o **temporizador** da partida.
- Organizar a **persistência do recorde** em arquivo e manter o código modular e testável.

## Status do desenvolvimento

- ✅ **Semana 1 — Proposta:** `docs/proposta.MD` com todos os itens pedidos.
- ✅ **Semana 2 — Protótipo:** janela Pygame, loop principal, grade 4×4, clique do mouse, lógica de pares, placar e código organizado em funções.

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
