# A-Maze-ing
*This is the way (Este é o caminho)*

**Resumo:** Crie seu próprio gerador de labirintos e exiba o resultado!
**Versão:** 2.2

---

## Índice
* **I** | Prefácio
* **II** | Instruções de IA
* **III** | Instruções Comuns
    * **III.1** | Regras Gerais
    * **III.2** | Makefile
    * **III.3** | Diretrizes Adicionais
* **IV** | Parte Obrigatória
    * **IV.1** | Resumo
    * **IV.2** | Uso
    * **IV.3** | Formato do arquivo de configuração
    * **IV.4** | Requisitos do Labirinto
    * **IV.5** | Formato do Arquivo de Saída
* **V** | Representação visual
* **VI** | Requisitos de reutilização de código
* **VII** | Requisitos do Readme
* **VIII** | Bônus
* **IX** | Submissão e avaliação por pares

---

## Capítulo I: Prefácio

Os labirintos fascinam os humanos há milhares de anos. Do lendário Labirinto de Cnossos na mitologia grega, construído por Dédalo para aprisionar o Minotauro, até os modernos livros de quebra-cabeças e videogames, os labirintos sempre simbolizaram mistério, desafio e design inteligente. Na ciência da computação, a geração de labirintos é mais do que apenas diversão: é uma aplicação prática de algoritmos, aleatoriedade e teoria dos grafos. Alguns algoritmos famosos usados para geração de labirintos, como o de Prim, Kruskal ou o *recursive backtracker*, também são usados em problemas do mundo real, como design de redes ou geração processual de conteúdo. Curiosamente, labirintos perfeitos (com um caminho único entre dois pontos quaisquer) estão diretamente relacionados a árvores geradoras (*spanning trees*) na teoria dos grafos. Construir um labirinto, especialmente um que você possa visualizar e compartilhar, é uma ótima maneira de explorar como os computadores podem criar estrutura a partir do caos, e se divertir um pouco enquanto faz isso.

> *"Um labirinto não é um lugar para se perder, mas um caminho a ser encontrado."*
> - Anônimo

---

## Capítulo II: Instruções de IA

### Contexto
Durante sua jornada de aprendizado, a IA pode auxiliar em diversas tarefas. Aproveite para explorar os vários recursos das ferramentas de IA e como elas podem apoiar seu trabalho. No entanto, aborde-as sempre com cautela e avalie criticamente os resultados. Quer se trate de código, documentação, ideias ou explicações técnicas, você nunca pode ter certeza absoluta de que sua pergunta foi bem formulada ou de que o conteúdo gerado é preciso. Seus colegas são um recurso valioso para ajudá-lo a evitar erros e pontos cegos.

### Mensagem principal
* Use a IA para reduzir tarefas repetitivas ou tediosas.
* Desenvolva habilidades de *prompting* (tanto para programação quanto para outras áreas) que beneficiarão sua futura carreira.
* Entenda como os sistemas de IA funcionam para prever e evitar melhor os riscos comuns, vieses e problemas éticos.
* Continue desenvolvendo habilidades técnicas e interpessoais trabalhando com seus colegas.
* Use apenas conteúdo gerado por IA que você compreenda totalmente e pelo qual possa assumir a responsabilidade.

### Regras do aluno:
* Você deve dedicar tempo para explorar as ferramentas de IA e entender como funcionam, para poder usá-las de forma ética e reduzir possíveis vieses.
* Você deve refletir sobre o seu problema antes de escrever o *prompt* – isso ajuda a criar *prompts* mais claros, detalhados e relevantes usando o vocabulário correto.
* Você deve desenvolver o hábito de verificar, revisar, questionar e testar sistematicamente qualquer coisa gerada pela IA.
* Você deve sempre buscar a revisão dos colegas – não dependa apenas da sua própria validação.

### Resultados da fase:
* Desenvolver habilidades de *prompting* de propósito geral e específicas de domínio.
* Aumentar sua produtividade com o uso eficaz de ferramentas de IA.
* Continuar fortalecendo o pensamento computacional, a resolução de problemas, a adaptabilidade e a colaboração.

### Comentários e exemplos:
* Você encontrará regularmente situações (exames, avaliações, etc.) em que precisará demonstrar compreensão real. Esteja preparado, continue desenvolvendo suas habilidades técnicas e interpessoais.
* Explicar seu raciocínio e debater com colegas frequentemente revela lacunas no seu entendimento. Faça do aprendizado entre pares uma prioridade.
* As ferramentas de IA geralmente não conhecem o seu contexto específico e tendem a dar respostas genéricas. Seus colegas, que compartilham o mesmo ambiente, podem oferecer visões mais relevantes e precisas.
* Enquanto a IA tende a gerar a resposta "mais provável", seus colegas podem fornecer perspectivas alternativas e nuances valiosas. Confie neles como um ponto de verificação de qualidade.

✅ **Boa prática:**
Pergunto à IA: "Como eu testo uma função de ordenação?". Ela me dá algumas ideias. Eu as testo e reviso os resultados com um colega. Refinamos a abordagem juntos.

❌ **Má prática:**
Peço à IA para escrever a função inteira e copio-colo no meu projeto. Durante a avaliação por pares, não consigo explicar o que ela faz ou o porquê. Perco a credibilidade e sou reprovado no projeto.

✅ **Boa prática:**
Uso a IA para ajudar no design de um *parser*. Depois, reviso a lógica com um colega. Encontramos dois bugs e reescrevemos juntos — melhor, mais limpo e totalmente compreendido.

❌ **Má prática:**
Deixo o Copilot gerar o código de uma parte crucial do meu projeto. Ele compila, mas não sei explicar como ele lida com os *pipes*. Durante a avaliação, não consigo me justificar e sou reprovado.

---

## Capítulo III: Instruções Comuns

### III.1 Regras Gerais
* Seu projeto deve ser escrito em Python 3.10 ou superior.
* Seu projeto deve aderir ao padrão de codificação `flake8`.
* Suas funções devem lidar com exceções de maneira elegante para evitar falhas (*crashes*). Use blocos `try-except` para gerenciar erros em potencial. Prefira gerenciadores de contexto (*context managers*) para recursos como arquivos ou conexões para garantir a limpeza automática. Se o seu programa falhar devido a exceções não tratadas durante a avaliação, ele será considerado não funcional.
* Todos os recursos (ex.: *file handles*, conexões de rede) devem ser gerenciados adequadamente para evitar vazamentos. Use *context managers* sempre que possível para manuseio automático.
* Seu código deve incluir *type hints* para parâmetros de funções, tipos de retorno e variáveis onde aplicável (usando o módulo `typing`). Use o `mypy` para verificação de tipo estática. Todas as funções devem passar pelo `mypy` sem erros.
* Inclua *docstrings* em funções e classes seguindo a PEP 257 (ex: estilo Google ou NumPy) para documentar propósito, parâmetros e retornos.

### III.2 Makefile
Inclua um `Makefile` no seu projeto para automatizar tarefas comuns. Ele deve conter as seguintes regras (a regra obrigatória `lint` implica as *flags* especificadas; é fortemente recomendado tentar `--strict` para verificações aprimoradas):
* `install`: Instala as dependências do projeto usando pip, uv, pipx, ou qualquer outro gerenciador de pacotes de sua escolha.
* `run`: Executa o script principal do seu projeto (ex: via interpretador Python).
* `debug`: Executa o script principal em modo de depuração usando o depurador integrado do Python (ex: pdb).
* `clean`: Remove arquivos temporários ou caches (ex: `__pycache__`, `.mypy_cache`) para manter o ambiente do projeto limpo.
* `lint`: Executa os comandos `flake8 .` e `mypy --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs .`
* `lint-strict` (opcional): Executa os comandos `flake8 .` e `mypy --strict .`

### III.3 Diretrizes Adicionais
* Crie programas de teste para verificar a funcionalidade do projeto (não serão enviados ou avaliados). Use frameworks como `pytest` ou `unittest` para testes unitários, cobrindo casos extremos (*edge cases*).
* Inclua um arquivo `.gitignore` para excluir artefatos do Python.
* É recomendado o uso de ambientes virtuais (ex: `venv` ou `conda`) para o isolamento de dependências durante o desenvolvimento.

*(Se houver requisitos adicionais específicos do projeto, eles serão declarados imediatamente abaixo desta seção).*

---

## Capítulo IV: Parte Obrigatória

### IV.1 Resumo
Você implementará um gerador de labirintos em Python que recebe um arquivo de configuração, gera um labirinto, possivelmente perfeito (com um único caminho entre a entrada e a saída), e o escreve em um arquivo usando uma representação hexadecimal de paredes. Você também fornecerá uma representação visual do labirinto e organizará seu código para que a lógica de geração possa ser reutilizada futuramente.

### IV.2 Uso
Seu programa deve ser executado com o seguinte comando:
```bash
python3 a_maze_ing.py config.txt
```
* `a_maze_ing.py` é o arquivo principal do seu programa. Você **deve** usar este nome.
* `config.txt` é o único argumento. É um arquivo de texto simples que define as opções de geração do labirinto. Você pode usar um nome de arquivo diferente.

Seu programa deve lidar com todos os erros com elegância: configuração inválida, arquivo não encontrado, sintaxe incorreta, parâmetros de labirinto impossíveis, etc. Ele **nunca** deve travar inesperadamente e deve **sempre** fornecer uma mensagem de erro clara ao usuário.

### IV.3 Formato do arquivo de configuração
O arquivo de configuração deve conter um par `CHAVE=VALOR` por linha.
Linhas que começam com `#` são comentários e devem ser ignoradas.

As seguintes chaves são obrigatórias:

| Chave | Descrição | Exemplo |
| :--- | :--- | :--- |
| `WIDTH` | Largura do labirinto (número de células) | `WIDTH=20` |
| `HEIGHT` | Altura do labirinto | `HEIGHT=15` |
| `ENTRY` | Coordenadas de entrada (x,y) | `ENTRY=0,0` |
| `EXIT` | Coordenadas de saída (x,y) | `EXIT=19,14` |
| `OUTPUT_FILE` | Nome do arquivo de saída | `OUTPUT_FILE=maze.txt` |
| `PERFECT` | O labirinto é perfeito? | `PERFECT=True` |

Você pode adicionar chaves extras (ex: `seed`, algoritmo, modo de exibição) se achar útil.
Um arquivo de configuração padrão deve estar disponível em seu repositório Git.

### IV.4 Requisitos do Labirinto
* O labirinto deve ser gerado aleatoriamente, mas a reprodutibilidade via *seed* é necessária.
* Cada célula do labirinto tem entre 0 e 4 paredes, em cada ponto cardeal (Norte, Leste, Sul, Oeste).
* O labirinto deve ser válido, o que significa:
  * A entrada e a saída existem, são diferentes, e estão dentro dos limites do labirinto.
  * A estrutura garante conectividade total e não possui células isoladas (exceto pelo padrão "42", veja abaixo).
  * Como a entrada e saída são células específicas, deve haver paredes nas bordas externas.
* Os dados gerados devem ser coerentes: cada célula vizinha deve ter a mesma parede compartilhada, se houver. Ex: é proibido ter uma primeira célula com uma parede no lado leste, e a segunda célula atrás daquela parede sem a parede no lado oeste.
* O labirinto não pode ter grandes áreas abertas. Corredores não podem ser mais largos que 2 células. Por exemplo, você pode ter uma área aberta de 2x3 ou 3x2, mas **nunca** uma área de 3x3.
* Ao ser representado visualmente (veja abaixo), o labirinto deve conter um "42" visível desenhado por várias células totalmente fechadas.
* Se a flag `PERFECT` estiver ativada, o labirinto deve conter exatamente um caminho entre a entrada e a saída (ou seja, deve ser um labirinto perfeito: nenhum loop/circuito).
* Se a flag `PERFECT` não estiver ativada (padrão), o labirinto deve ser um tabuleiro diretamente utilizável para um jogo estilo Pac-Man. Concretamente:
  * Todo corredor é alcançável (conectividade total), de forma que todo o tabuleiro possa ser preenchido com "pac-gums" e continue sendo possível vencer o jogo;
  * Os quatro cantos e o centro são corredores abertos (os fantasmas e super-pac-gums ficam nos cantos, o jogador começa no centro);
  * Oferece pelo menos duas rotas independentes (loops), para que um jogador perseguido sempre tenha uma alternativa (um labirinto perfeito, ou um labirinto perfeito com apenas uma parede removida, **não** é aceitável neste modo);
  * Caminhos sem saída (*dead-ends*) devem ser raros (alguns são tolerados); um tabuleiro sem nenhum caminho sem saída é o ideal e é recompensado como bônus (veja o capítulo de Bônus).

> **Nota:** O padrão "42" pode ser omitido caso o tamanho do labirinto não permita (ou seja, muito pequeno). Imprima uma mensagem de erro no console nesse caso.

### IV.5 Formato do Arquivo de Saída
O labirinto deve ser gravado no arquivo de saída usando um dígito hexadecimal por célula, onde cada dígito codifica quais paredes estão fechadas:

| Bit | Direção |
| :--- | :--- |
| 0 (LSB) | Norte |
| 1 | Leste |
| 2 | Sul |
| 3 | Oeste |

* Uma parede fechada define o bit como 1, aberta significa 0.
  * *Exemplo:* `3` (binário `0011`) significa que as paredes estão abertas para o sul e oeste (bits 0 e 1, relativos a Norte e Leste, estão setados em 1). Ou `A` (binário `1010`) significa que as paredes leste e oeste estão fechadas.
* As células são armazenadas linha por linha, uma linha por linha de texto.
* Após uma linha vazia, os 3 elementos a seguir são inseridos no arquivo de saída em 3 linhas:
  * as coordenadas de entrada;
  * as coordenadas de saída;
  * o caminho válido mais curto da entrada à saída, usando as quatro letras N, E, S, W.
* Todas as linhas devem terminar com um `\n`.

*(O documento menciona um script `maze_analyzer.py` fornecido que pode validar esses arquivos automaticamente).*

---

## Capítulo V: Representação visual
Seu programa deve fornecer uma maneira de exibir o labirinto visualmente, usando:
* Renderização ASCII no terminal, **ou**
* Um display gráfico usando a biblioteca MiniLibX (MLX).

O visual deve mostrar claramente as paredes, a entrada, a saída e o caminho da solução.

As interações do usuário devem estar disponíveis, no mínimo para as seguintes tarefas:
* Gerar novamente um novo labirinto e exibi-lo.
* Mostrar/Ocultar o caminho válido mais curto da entrada à saída.
* Mudar as cores das paredes do labirinto.
* *Opcional:* definir cores específicas para exibir o padrão "42".

Você pode adicionar interações extras para o usuário.

---

## Capítulo VI: Requisitos de reutilização de código
Você deve implementar a geração do labirinto como uma classe única (ex: `MazeGenerator`) dentro de um módulo independente que possa ser importado em um projeto futuro.

Você deve fornecer uma breve documentação descrevendo como:
* Instanciar e usar seu gerador, com pelo menos um exemplo básico.
* Passar parâmetros personalizados (ex: tamanho, seed).
* Acessar a estrutura gerada, e acessar pelo menos uma solução.

> *Nota: O módulo do gerador concede acesso à estrutura do labirinto, mas não é necessariamente o mesmo formato do arquivo de saída.*

Este módulo reutilizável completo (código e documentação) deve estar disponível em um único arquivo adequado para posterior instalação pelo `pip`.
Este pacote deve ser chamado `mazegen-*` e o arquivo deve estar localizado na raiz do seu repositório git.
Tanto a extensão `.tar.gz` quanto `.whl` são permitidas, conforme gerado pelo build padrão de um pacote Python.
*(Exemplo de nome de arquivo completo: `mazegen-1.0.0-py3-none-any.whl`).*

Você deve fornecer no seu repositório Git todos os elementos necessários para construir (build) o pacote. Isso será solicitado durante a avaliação: em um ambiente virtual ou equivalente, instale as ferramentas necessárias e construa seu pacote novamente a partir dos fontes.

Como este gerador de labirintos destina-se a ser reutilizado em um projeto posterior, você deve incluir um arquivo `LICENSE.md` na raiz do seu repositório, declarando a licença sob a qual o seu código pode ser reutilizado. Escolher e escrever essa licença faz parte da tarefa: é seu primeiro contato com licenciamento de software e propriedade intelectual. A licença que você escolher deve permitir explicitamente a reutilização e distribuição do seu gerador por projeto(s) futuro(s) que dependam dele.

O arquivo principal `README.md` (que não faz parte do módulo reutilizável) também deve conter essa breve documentação.

---

## Capítulo VII: Requisitos do Readme
Um arquivo `README.md` deve ser fornecido na raiz do seu repositório Git. Seu propósito é permitir que qualquer pessoa não familiarizada com o projeto (colegas, equipe, recrutadores, etc.) entenda rapidamente do que se trata o projeto, como executá-lo e onde encontrar mais informações sobre o tópico.

O `README.md` deve incluir pelo menos:
* A primeira linha deve ser em itálico e dizer: *This project has been created as part of the 42 curriculum by <login1>, <login2>[, <login3>[...]].*
* Uma seção "Descrição" que apresente claramente o projeto, incluindo seu objetivo e uma breve visão geral.
* Uma seção "Instruções" contendo informações relevantes sobre compilação, instalação e/ou execução.
* Uma seção "Recursos" listando referências clássicas relacionadas ao tópico (documentação, artigos, tutoriais, etc.), além de uma descrição de como a IA foi usada — especificando para quais tarefas e em quais partes do projeto.

Adições requeridas específicas deste projeto:
* A estrutura completa e o formato do seu arquivo de configuração.
* O algoritmo de geração de labirinto que você escolheu.
* Por que você escolheu este algoritmo.
* Qual parte do seu código é reutilizável, e como.
* O gerenciamento da sua equipe e projeto, incluindo:
  * Os papéis de cada membro da equipe.
  * Seu planejamento antecipado e como ele evoluiu até o fim.
  * O que funcionou bem e o que poderia ser melhorado.
  * Você usou alguma ferramenta específica? Quais?

Se você implementar recursos avançados (múltiplos algoritmos, opções de exibição), descreva-os no `README.md`.
*O inglês é recomendado; alternativamente, você pode usar o idioma principal do seu campus.*

---

## Capítulo VIII: Bônus
Você pode adicionar vários bônus ao seu projeto. Aqui estão possíveis exemplos:
* Um labirinto padrão (não-perfeito) **sem nenhum caminho sem saída**: um tabuleiro perfeitamente "trançado", para que um jogador perseguido nunca fique encurralado (o script de análise fornecido confirma isso com `--max-dead-ends 0`).
* Suporte a múltiplos algoritmos de geração de labirintos.
* Adicionar animação durante a geração do labirinto.

---

## Capítulo IX: Submissão e avaliação por pares
Envie sua tarefa em seu repositório Git como de costume. Apenas o trabalho dentro do seu repositório será avaliado durante a defesa. Não hesite em verificar novamente os nomes dos seus arquivos para garantir que estejam corretos.

Durante a avaliação, uma breve modificação do projeto pode ser solicitada ocasionalmente. Isso pode envolver uma pequena mudança de comportamento, algumas linhas de código para escrever ou reescrever, ou um recurso fácil de adicionar.
Embora esta etapa possa não ser aplicável a todos os projetos, você deve estar preparado para ela se for mencionada nas diretrizes de avaliação.

Esta etapa serve para verificar sua compreensão real de uma parte específica do projeto. A modificação pode ser feita em qualquer ambiente de desenvolvimento de sua escolha (ex: seu setup habitual), e deve ser viável em poucos minutos, a menos que um prazo específico seja definido como parte da avaliação.

Você pode, por exemplo, ser solicitado a fazer uma pequena atualização em uma função ou script, modificar uma exibição ou ajustar uma estrutura de dados para armazenar novas informações, etc.
Os detalhes (escopo, alvo, etc.) serão especificados nas diretrizes de avaliação e podem variar de uma avaliação para outra para o mesmo projeto.
