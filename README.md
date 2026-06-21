# MemoryPy

**MemoryPy** é um **Jogo da Memória** desenvolvido em **Python** com a biblioteca **Pygame**, como projeto final da disciplina de **Introdução a Algoritmos / Programação** (PUC Minas — CDIA).

O jogador escolhe uma dificuldade no menu, vira cartas em uma grade e precisa encontrar todos os pares iguais antes que o tempo da partida acabe. O projeto foi construído a partir do template oficial da disciplina, com foco em código organizado, modular e coerente com os conteúdos estudados.

## Integrantes do grupo

- Mario
- Guilherme
- Matheus
- Rafael

## Sobre o jogo

Ao abrir, o jogo mostra um **menu** onde o jogador escolhe a dificuldade, o modo (1 ou 2 jogadores) e se quer jogar com **cartas especiais**. Em seguida aparece o tabuleiro com as cartas viradas para baixo. A cada turno, o jogador clica em **duas cartas** para revelá-las:

- Se as duas cartas forem **iguais**, elas permanecem abertas (com um brilho ao redor) e o jogador soma pontos.
- Se forem **diferentes**, voltam a ficar ocultas após uma breve pausa (~0,7 s), exigindo que o jogador memorize as posições.

Cada carta tem um **ícone** (forma + cor), no lugar de uma letra, para facilitar achar os pares. O desafio é completar o tabuleiro **antes do tempo acabar**, usando a memória para reduzir o número de tentativas.

### Níveis de dificuldade

O jogador escolhe entre quatro níveis no menu. Cada nível tem grade, tempo e peso de pontuação próprios, e guarda o **recorde separadamente**:

| Nível | Grade | Pares | Tempo | Peso (pontos) |
|-------|-------|-------|-------|----------------|
| Fácil | 4×4 | 8 | 90 s | 1× |
| Médio | 4×4 | 8 | 60 s | 1× |
| Difícil | 4×6 | 12 | 60 s | 2× |
| Extremo | 6×6 | 18 | 45 s | 3× |

### Modos de jogo

- **1 Jogador:** o modo padrão, descrito no restante deste README (pontos, combo, dicas, recorde, ranking, conquistas).
- **2 Jogadores:** os jogadores se alternam clicando nas cartas. Quem acerta um par marca os pontos **e joga de novo**; quem erra passa a vez. Vence quem tiver mais pontos quando o tabuleiro acabar. Esse modo não usa recorde, ranking, conquistas nem combo — é só a pontuação dos dois jogadores na partida.

### Cartas especiais (opcional)

Quando a opção **"Especiais: Ligadas"** está marcada no menu (só no modo 1 jogador, ou também no 2 jogadores), três dos pares do nível são substituídos por cartas com efeito:

| Carta | Ícone | Efeito ao formar o par |
|-------|-------|--------------------------|
| Curinga | estrela dourada | Completa automaticamente outro par que ainda está oculto |
| Bônus de tempo | cruz verde | Soma 10 segundos ao tempo da partida |
| Embaralha | hexágono roxo | Sorteia uma nova posição para os valores das cartas ainda ocultas |

### Como o jogador interage

| Ação | Comando |
|------|---------|
| Selecionar / revelar uma carta | **Clique esquerdo do mouse** |
| Escolher dificuldade, modo, opções e botões | **Clique esquerdo do mouse** |
| Pausar / retomar a partida | Tecla **P** |
| Reiniciar a partida | Tecla **R** |
| Usar uma dica (1 jogador, máx. 3 por partida) | Tecla **H** |
| Trocar entre tema claro e escuro | Tecla **T** |
| Ligar/desligar o som | Tecla **S** |
| Voltar ao menu (na pausa ou no fim) | Tecla **M** |
| Pausar (em jogo) ou sair (nas outras telas) | Tecla **ESC** |

### Objetivo

Encontrar todos os pares de cartas iguais no menor número de tentativas possível, concluindo o tabuleiro antes que o cronômetro chegue a zero.

### Regras

- O tabuleiro é embaralhado a cada partida, com o tamanho definido pela dificuldade.
- O jogador revela **duas cartas por turno**.
- **Par igual:** as cartas ficam abertas e somam pontos (10 × peso do nível × multiplicador do combo).
- **Par diferente:** as cartas voltam a ficar ocultas após a pausa.
- **Combo:** acertar pares em sequência aumenta um multiplicador de pontos (até 3×); errar zera o combo.
- **Dica:** revela rapidamente um par oculto por 1 segundo, custando 5 pontos. No máximo 3 por partida.
- A partida tem **tempo limitado**, que varia conforme o nível (e pode aumentar com a carta especial de bônus de tempo).
- Ao vencer, sobra de tempo vira **pontos de bônus** (2 × peso por segundo restante).

### Condições de vitória e derrota

- **Vitória:** todos os pares são encontrados antes do tempo acabar. Aparece a tela "Você venceu!" com pontos, tempo, recorde, precisão da partida, estatísticas pessoais do nível, conquistas novas e o ranking — com um campo para digitar o nome, se a pontuação entrar no top 5.
- **Derrota:** o tempo da partida se esgota antes de completar o tabuleiro. Aparece a tela "Tempo esgotado!".
- Em ambos os casos, o jogador pode pressionar **R** para jogar de novo ou **M** para voltar ao menu.

### O que aparece na tela

Na faixa superior (placar) são exibidos, em tempo real:

- **Tentativas**, **Pontos**, **Tempo** restante e **Recorde** do nível
- O nível atual, o **combo** atual e quantas **dicas** ainda restam
- No modo 2 jogadores: a pontuação de cada jogador e de quem é a vez

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

Saída esperada: todos os testes passando (atualmente **31 testes**).

## Observações de execução

- Em alguns sistemas (Linux/macOS), use `python3` e `pip3` no lugar de `python` e `pip`.
- No Linux com sessão **Wayland**, se aparecer o erro `pygame.error: windows not available`, rode o jogo assim: `SDL_VIDEODRIVER=x11 python main.py`.
- Se o computador não tiver placa de som (ou em ambientes de teste), o jogo detecta isso e simplesmente não toca nenhum som, sem travar.

## Estrutura do projeto

```
MemoryGame-main/
├── main.py              # Ponto de entrada: inicia o jogo
├── requirements.txt     # Dependências (pygame, pytest)
├── README.md            # Este arquivo
├── .gitignore           # Arquivos ignorados pelo Git
├── scripts/
│   └── gerar_sons.py    # Gera os efeitos sonoros e a música (assets/sons/*.wav)
├── src/                 # Código-fonte do jogo
│   ├── __init__.py      # Torna 'src' um pacote Python
│   ├── jogo.py          # Loop principal, eventos, telas (menu, pausa, derrota)
│   ├── config.py        # Configurações: tela, cores, temas, níveis, cartas especiais
│   ├── funcoes.py       # Lógica do jogo (funções puras, testáveis)
│   ├── sprites.py       # Desenho das cartas (ícones, animação, brilho) e dos textos
│   ├── tela_vitoria.py  # Telas de comemoração (1 e 2 jogadores)
│   ├── dados.py         # Leitura e escrita de recordes, estatísticas, ranking e conquistas
│   └── audio.py         # Efeitos sonoros e música de fundo
├── assets/
│   ├── imagens/         # Spritesheet do template (não usada nas cartas, ver "Assets externos")
│   └── sons/            # Efeitos sonoros e música, gerados por scripts/gerar_sons.py
├── data/                # Arquivos persistentes
│   └── record.json      # Recordes, estatísticas, ranking e conquistas (ignorado pelo Git)
├── tests/               # Testes automatizados (pytest)
│   └── test_logica.py   # Testes das funções de lógica
└── docs/                # Documentação
    └── proposta.MD      # Proposta inicial (Semana 1)
```

## Organização do código

O projeto é dividido em módulos com responsabilidades claras:

- **`main.py`** — ponto de entrada; apenas chama `executar_jogo()`.
- **`src/config.py`** — todas as constantes em um só lugar: tamanho da janela, cores, temas (claro/escuro), níveis de dificuldade, ícones das cartas, cartas especiais, combo, dica e caminho dos dados salvos.
- **`src/funcoes.py`** — a **lógica pura** do jogo, em funções independentes do Pygame (por isso são fáceis de testar): embaralhar as cartas, comparar um par, calcular pontos e combo, calcular precisão, atualizar estatísticas, verificar conquistas e atualizar o ranking.
- **`src/sprites.py`** — a parte visual das cartas: desenha o ícone ou o "?" conforme o estado, a animação de virar e o brilho ao formar um par.
- **`src/tela_vitoria.py`** — as telas de comemoração mostradas ao vencer (uma para 1 jogador, com ranking e conquistas, e outra mais simples para 2 jogadores).
- **`src/dados.py`** — persistência: lê e grava recordes, estatísticas, ranking, conquistas e preferências (tema/som), todos no mesmo arquivo JSON.
- **`src/audio.py`** — liga o som do Pygame e toca os efeitos e a música, sem travar o jogo caso não haja som disponível.
- **`src/jogo.py`** — o **loop principal**: trata eventos (mouse e teclado), controla os turnos, o temporizador, a pausa, o combo, as dicas, as cartas especiais, os dois modos de jogo e a renderização de cada tela.

## Conceitos da disciplina aplicados

| Conceito | Onde aparece no projeto |
|----------|--------------------------|
| Variáveis e entrada/saída | Estado da partida e leitura de cliques/teclas |
| Estruturas condicionais | Comparação de pares, efeitos das cartas especiais, vitória/derrota |
| Laços de repetição | Loop principal, montagem do tabuleiro, ordenação do ranking |
| Listas | Tabuleiro, ranking de cada nível |
| Dicionários | Cada carta, o estado da partida e os dados salvos em JSON |
| Tuplas | Coordenada `(linha, coluna)` de cada carta |
| Conjuntos | Pares já encontrados, conquistas desbloqueadas |
| Funções e modularização | Código dividido em módulos com funções específicas |
| Leitura e escrita de arquivos | Recordes, estatísticas, ranking e conquistas em `data/record.json` |
| Testes automatizados | `tests/test_logica.py` com pytest (31 testes) |

### Estruturas de dados utilizadas

- **Lista** — `tabuleiro`, a sequência das cartas da partida; o ranking de cada nível.
- **Dicionário** — cada carta é um dicionário (`valor`, `posicao`, `rect`, `revelada`, `encontrada`); o estado da partida, os recordes, as estatísticas e o ranking também são dicionários.
- **Tupla** — a posição de cada carta na grade, no formato `(linha, coluna)`.
- **Conjunto** — `pares_encontrados`, registrando os símbolos já combinados; `conquistas`, registrando as conquistas já desbloqueadas.

### Leitura e escrita de arquivos

Todos os dados do jogador ficam em `data/record.json`, com uma seção para cada coisa:

```json
{
  "recordes": { "facil": 80, "extremo": 260 },
  "estatisticas": { "facil": { "partidas": 5, "vitorias": 4, "menor_tentativas": 9, "melhor_tempo": 35 } },
  "ranking": { "facil": [ { "nome": "Mario", "pontos": 200 } ] },
  "conquistas": ["perfeito", "sobrou_tempo"],
  "preferencias": { "tema": "escuro", "som_ativado": true }
}
```

Ao abrir o jogo, esses dados são carregados; cada seção é lida e gravada separadamente (ver `src/dados.py`), para uma não sobrescrever a outra. Se o arquivo não existir ainda, o jogo começa do zero (sem recordes, estatísticas, ranking ou conquistas).

## Uso do template da disciplina

O projeto foi desenvolvido **a partir do template oficial** ([IntroAlgs_pygame_template](https://github.com/ICEI-PUC-Minas-PPL-CDIA/IntroAlgs_pygame_template)), mantendo a estrutura de pastas e os arquivos base. O grupo **adaptou e reescreveu** o conteúdo dos módulos de `src/` para implementar a mecânica do jogo da memória, preservando a organização original do repositório.

## Assets externos

- **Sons:** `acerto.wav`, `erro.wav`, `vitoria.wav` e `musica_fundo.wav` (pasta `assets/sons/`) não são sons de terceiros — são tons sintetizados por código (ondas senoidais simples) pelo script `scripts/gerar_sons.py`, sem nenhuma licença envolvida.
- **Ícones das cartas:** desenhados em código com formas geométricas do próprio Pygame (igual às estrelas da tela de vitória), no lugar de imagens externas.
- **Spritesheet (`assets/imagens/spritesheet.bmp`):** veio junto do template oficial da disciplina, mas não é usada nas cartas — ela é um conjunto genérico de personagens e inimigos (não tem ícones suficientes e parecidos com os necessários para os símbolos do jogo), então optamos por manter os ícones desenhados em código.

| Recurso | Tipo | Fonte / Autor | Licença |
|---------|------|---------------|---------|
| `spritesheet.bmp` | Imagem (não usada nas cartas) | Template oficial da disciplina | Uso educacional do template |
| Demais sons e ícones | Gerados por código | Próprio grupo | Não se aplica (sem terceiros) |

## Principais desafios

- Implementar a **pausa entre cartas erradas** sem travar o loop do jogo (resolvido controlando o tempo por marcação de instante, não com `sleep`).
- Fazer o **cronômetro continuar certo após a pausa**, descontando o tempo parado.
- Sincronizar a **lógica de turnos** (duas cartas por jogada) com o **temporizador** da partida.
- Montar a grade de forma que **cartas e fonte se ajustem** ao tamanho de cada nível.
- Organizar a **persistência dos dados por nível** (recorde, estatísticas, ranking) sem misturar as seções do arquivo.
- Garantir que a **carta curinga** nunca deixe um par "sobrando" sem parceiro no tabuleiro (testamos isso simulando 200 partidas automáticas).
- Separar o que é **regra de jogo** (pode ser testado sem abrir a janela) do que é **só desenho** (animação, ícones, telas), mesmo com mais funcionalidades.

## Status do desenvolvimento

- ✅ **Semana 1 — Proposta:** `docs/proposta.MD` com todos os itens pedidos.
- ✅ **Semana 2 — Protótipo:** janela Pygame, loop principal, grade 4×4, clique do mouse, lógica de pares, placar e código organizado em funções.
- ✅ **Semana 3 — Interações e regras:** menu de dificuldade, quatro níveis com grade dinâmica, pausa, bônus de tempo, telas de vitória/derrota, recordes por nível em arquivo e testes automatizados.
- ✅ **Semana 4 — Entrega final:** ícones nas cartas, animação de virar e brilho, temas claro/escuro, efeitos sonoros e música, combo de pontos, sistema de dica, cartas especiais, modo 2 jogadores, estatísticas pessoais, conquistas e ranking com nome do jogador.

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

## Melhorias da seção 17 implementadas nesta entrega

Todas as ideias listadas na seção 17 da proposta (`docs/proposta.MD`) foram implementadas até esta entrega final:

- **Jogabilidade:** menu com tela de pausa (semana 3), níveis de dificuldade (semana 3), modo 2 jogadores, sistema de dica, combo/multiplicador e cartas especiais (curinga, bônus de tempo, embaralha).
- **Visual e áudio:** animação de virar as cartas e brilho ao formar par, efeitos sonoros e música de fundo, temas claro/escuro, ícones nas cartas no lugar das letras.
- **Progressão e dados:** ranking com nome do jogador, estatísticas pessoais (melhor tempo, menor número de tentativas, total de partidas) e conquistas.
- **Pontuação e feedback:** bônus de pontuação pelo tempo restante (semana 3), cálculo de precisão e tela de comemoração na vitória (semana 3, ampliada nesta entrega).

Não restou nenhuma ideia da seção 17 fora do jogo.

## Decisões técnicas

Algumas escolhas que o grupo fez durante o desenvolvimento e o motivo de cada uma:

- **Separar lógica e visual:** as regras do jogo ficam em `funcoes.py` (sem Pygame) e o desenho em `sprites.py`/`tela_vitoria.py`. Isso deixa o código organizado e permite testar a lógica sem abrir a janela.
- **Guardar tudo num "estado":** os dados que mudam durante a partida (cartas, pontos, tempo, situação) ficam num único dicionário. Assim, reiniciar a partida é só criar um estado novo.
- **Um arquivo JSON, várias seções:** em vez de um arquivo por tipo de dado, usamos `data/record.json` com uma chave para recordes, estatísticas, ranking, conquistas e preferências, lidas e gravadas separadamente.
- **Tempo controlado por marcação, não por `sleep`:** a pausa entre cartas erradas, a dica e o cronômetro usam o relógio do Pygame em vez de travar o programa, para o jogo continuar respondendo.
- **Curinga sem deixar par "órfão":** em vez da curinga combinar com qualquer carta (o que poderia deixar uma carta sem par para sempre), ela forma par com a outra curinga e, ao acertar, completa sozinha outro par que já existe no tabuleiro. Assim o tabuleiro sempre pode ser fechado.
- **Sons gerados por código:** para não depender de músicas ou efeitos de terceiros (e da licença deles), os sons são tons simples gerados com seno, salvos como `.wav` por `scripts/gerar_sons.py`.
- **Ícones desenhados em código:** cada símbolo tem uma forma e cor fixas (círculo, estrela, cruz, etc.), desenhadas com `pygame.draw`, no mesmo estilo que já era usado para as estrelas da tela de vitória — sem depender de imagens externas.
