# Proposta Inicial do Jogo

Documento da Semana 1 do projeto da disciplina de Introdução a Algoritmos / Programação (PUC Minas — CDIA), desenvolvido com Python e Pygame.

## 1. Nome provisório do jogo

> **MemoryPy** — Jogo da Memória

## 2. Integrantes do grupo

- Mario
- Guilherme
- Matheus
- Rafael

## 3. Tipo de jogo

Tipo escolhido pelo grupo:

> Jogo de memória (combinação de pares de cartas).

## 4. Descrição geral do jogo

Descrição:

> Na tela aparece uma grade de **4×4 cartas (16 cartas, 8 pares)**, todas viradas para baixo. O jogador controla o jogo apenas com o mouse: a cada turno, ele clica em duas cartas para revelá-las. Se as duas cartas formarem um par igual, elas permanecem abertas e o jogador soma pontos. Se forem diferentes, elas voltam a ficar ocultas após uma breve pausa, exigindo que o jogador memorize as posições. O desafio principal é encontrar todos os pares antes que o tempo da partida se esgote, usando a memória para reduzir o número de tentativas.

## 5. Objetivo do jogador

Objetivo:

> Encontrar todos os 8 pares de cartas iguais no menor número de tentativas possível, concluindo o tabuleiro antes que o tempo acabe.

## 6. Regras principais

Regras do grupo:

- Regra 1: O tabuleiro é uma grade 4×4 com 8 pares de cartas viradas para baixo.
- Regra 2: A cada turno o jogador clica em duas cartas, que são reveladas.
- Regra 3: Se as duas cartas forem iguais, elas permanecem abertas e o jogador pontua.
- Regra 4: Se as duas cartas forem diferentes, elas voltam a ficar ocultas após uma breve pausa.
- Regra 5: A partida termina quando todos os pares são encontrados (vitória) ou quando o tempo acaba (derrota).

## 7. Condição de vitória

Condição de vitória:

> O jogador vence ao encontrar todos os 8 pares (revelar e combinar todas as 16 cartas) antes do tempo da partida se esgotar.

## 8. Condição de derrota ou encerramento

Condição de derrota ou encerramento:

> O jogador perde se o tempo da partida acabar antes de todos os pares serem encontrados. A partida também pode ser reiniciada a qualquer momento pelo jogador (tecla R) ou encerrada com ESC.

## 9. Elementos previstos no jogo

### Jogador ou elemento principal

Descrição:

> Não há um personagem controlado. O jogador interage diretamente com as cartas do tabuleiro usando o cursor do mouse.

### Obstáculos, inimigos ou desafios

Descrição:

> O principal desafio é o **tempo limitado** combinado com a necessidade de **memorizar** as posições das cartas já reveladas. Quanto mais erros, mais tempo é gasto e maior a chance de derrota.

### Itens, alvos ou objetos de interação

Descrição:

> As 16 cartas do tabuleiro, organizadas em 8 pares. Cada carta possui um valor/símbolo e dois estados: oculta (virada para baixo) e revelada (virada para cima).

### Pontuação, vidas, tempo ou progresso

Descrição:

> O jogador não tem vidas. O progresso é medido pela quantidade de pares encontrados e pela pontuação acumulada. Um cronômetro/tempo regressivo controla a duração da partida, e a melhor pontuação é registrada como recorde persistente.

## 10. Controles previstos

Controles do grupo:

- Clique esquerdo do mouse: selecionar/revelar uma carta.
- Tecla R: reiniciar a partida.
- Tecla ESC: sair do jogo.

## 11. Organização inicial do código

Organização planejada:

> - `main.py`: ponto de entrada que inicia o jogo;
> - `src/jogo.py`: contém o loop principal e o controle de estados (turnos, vitória, derrota);
> - `src/config.py`: guarda configurações como tamanho da tela, cores e tempo;
> - `src/funcoes.py`: funções auxiliares (embaralhar cartas, comparar pares, calcular pontuação);
> - `src/sprites.py`: representação visual das cartas;
> - `src/dados.py`: funções de leitura e escrita do arquivo de recorde.

## 12. Estruturas de dados que poderão ser utilizadas

- **Lista:** armazenar as cartas do tabuleiro (ordem das cartas na grade).
- **Dicionário:** associar valores/símbolos às cartas e organizar o recorde salvo em arquivo (formato JSON).
- **Tupla:** representar as coordenadas `(linha, coluna)` de cada carta na grade.
- **Conjunto:** registrar os pares já encontrados, evitando repetições.

## 13. Uso previsto de arquivos

> O jogo fará **leitura e escrita** de um arquivo de recorde em `data/record.json`. Ao iniciar, o recorde salvo é carregado; ao final de uma partida, se a pontuação superar o recorde, o arquivo é atualizado. O uso de JSON permite estruturar os dados (por exemplo, melhor pontuação e tempo) de forma organizada.

## 14. Testes planejados

Testes automatizados com **pytest**:

- Verificar se o **embaralhamento** gera exatamente 8 pares corretos no tabuleiro.
- Validar a **lógica de comparação de pares** (duas cartas iguais combinam; diferentes não).
- Conferir o **cálculo de pontuação** a cada par encontrado.
- Garantir a **atualização do recorde** apenas quando a nova pontuação é maior que a salva.

## 15. Principais dificuldades esperadas

Dificuldades previstas:

- Dificuldade 1: Controlar a pausa entre revelar duas cartas diferentes e voltá-las a ocultar sem travar o loop do jogo.
- Dificuldade 2: Sincronizar a lógica de turnos (dois cliques por jogada) com o controle de tempo.
- Dificuldade 3: Persistir e atualizar corretamente o recorde em arquivo, além de organizar o código e o uso do GitHub em grupo.

## 16. Escopo mínimo para a entrega final

Escopo mínimo:

> A versão mínima terá: tabuleiro 4×4 com 8 pares embaralhados, revelação de duas cartas por clique do mouse, comparação de pares, contagem de pontuação, controle de tempo, telas de vitória e derrota, reinício com a tecla R e registro do recorde em arquivo.

## 17. Possíveis melhorias, caso haja tempo

Caso o grupo tenha tempo após concluir o escopo mínimo, pensamos em várias ideias para deixar o jogo mais completo e divertido. Elas estão organizadas por tema:

### Jogabilidade

- Tela inicial (menu) com opções de jogar, ver recorde e sair, além de uma tela de pausa.
- Níveis de dificuldade: grades maiores (4×6, 6×6) e tempo mais curto, com o número de pares ajustado automaticamente.
- Modo dois jogadores, alternando turnos e contando os pares de cada um separadamente.
- Sistema de dica: revela rapidamente um par ainda oculto em troca de pontos.
- Combo/multiplicador: acertos seguidos valem cada vez mais pontos; um erro zera o combo.
- Cartas especiais (curinga que combina com qualquer carta, bônus de tempo ou "embaralha tudo").

### Visual e áudio

- Animação de virar as cartas (efeito de flip) e um brilho ao formar um par.
- Efeitos sonoros para acerto, erro e vitória, além de uma música de fundo.
- Temas visuais alternáveis (paletas de cores diferentes, modo claro/escuro).
- Usar imagens nas cartas (a partir da spritesheet) no lugar das letras.

### Progressão e dados

- Ranking com o nome do jogador salvo em JSON, exibindo as melhores partidas.
- Estatísticas pessoais: melhor tempo, menor número de tentativas e total de partidas jogadas.
- Conquistas/medalhas (por exemplo, "venceu sem errar" ou "venceu com mais de 30s sobrando").

### Pontuação e feedback

- Bônus de pontuação proporcional ao tempo restante no fim da partida.
- Cálculo de precisão (porcentagem de acertos sobre o total de tentativas).
- Tela de comemoração na vitória, mostrando pontos, tempo e se houve novo recorde.

> **Observação (atualização da Semana 3):** algumas dessas melhorias já foram
> implementadas no jogo — o **menu inicial**, a **tela de pausa**, os **níveis de
> dificuldade** (4×4, 4×6 e 6×6), o **bônus de pontuação pelo tempo restante** e a
> **tela de comemoração na vitória** (com aviso de novo recorde). Os recordes
> passaram a ser guardados **por nível** no arquivo `data/record.json`.
>
> **Observação (entrega final — Semana 4):** todas as ideias restantes desta
> seção foram implementadas. Em **Jogabilidade**: modo **dois jogadores**,
> **sistema de dica**, **combo/multiplicador** de pontos e **cartas especiais**
> (curinga, bônus de tempo e embaralha — adaptamos a curinga para completar
> sozinha outro par oculto, em vez de combinar com qualquer carta, para o
> tabuleiro nunca ficar com um par "órfão" sem solução). Em **Visual e áudio**:
> **animação de virar as cartas** e brilho ao formar par, **efeitos sonoros e
> música de fundo** (gerados por código, sem depender de arquivos de
> terceiros) e **temas claro/escuro**; no lugar de usar a spritesheet do
> template (que não tinha ícones combinando com o jogo), desenhamos **ícones
> próprios** (forma + cor) para cada carta. Em **Progressão e dados**:
> **ranking com nome do jogador**, **estatísticas pessoais** (melhor tempo,
> menor número de tentativas, total de partidas) e **conquistas**. Em
> **Pontuação e feedback**: **cálculo de precisão** da partida. Detalhes de
> cada funcionalidade estão no `README.md`.
