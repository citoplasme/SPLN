# Identificação de Interações entre Personagens num Livro 

O primeiro projeto prático da Unidade Curricular de __Scripting no Processamento de Linguagem Natural__ consistiu em identificar interações entre personagens de um livro. Para isso, foi definido que uma interação seria o aparecimento do nome das personagens numa mesma frase.  

Dito isto, a linha de pensamento para a resolução do problema passou por começar por identificar os nomes com base numa expressão regular. Em seguida, as frases, bem como definir que palavras maiúsculas no início da frase seriam descartadas de forma a reduzir a aumentar a capacidade de deteção de casos reais.  

Tendo o texto dividido em frases, foram efetuadas as combinações das personagens nelas presentes, recorrendo ao módulo __itertools__. Note-se que existe a possibilidade de a mesma personagem ser detetada mais do que uma vez numa só frase, pelo que este caso foi tratado antes de se efetuarem as combinações, tirando proveito do conceito de _set_.    

Cada combinação representa uma interação entre duas personagens, pelo que se deve incrementar o contador de interações entre as mesmas. Para isso, foi utilizado um dicionário, em que a chave são os dois nomes das personagens no formato __{Nome 1}{Nome 2}__. Como seria de esperar, o valor associado a cada chave trata-se do número de interações entre aquelas personagens. Note-se, ainda, que existem certas deteções falsas que se tratam de, por exemplo, pronomes, pelo que é efetuada uma filtração para os remover antes da realização das combinações.  

Por fim, de modo a representar de forma simples e rápida os resultados, o dicionário é convertido num grafo onde cada nodo corresponde a uma personagem. Este pode possuir várias ligações a outros nodos, sendo estas caraterizadas por um peso, tratando-se este do número de interações entre os dois nodos.

## Funcionalidades

### Calcular as relações entre (N1, N2)*

- De modo a calcular as relações entre nodos utilizou-se um dicionário como mencionado anteriormente. A utilização deste dicionário permitiu aplicar de forma simples métodos de redução de tamanho, bem como a atualização regular do número de interações. Finalizada a análise do texto, o dicionário foi convertido num grafo, sendo este responsável pela representação das relações entre nodos, como pretendido.  

### Definir _reduce size strategies_
 
 - Os métodos de redução de tamanho permitem uma limpeza de certos valores que são derivados da deteção de nomes. Estes valores podem tratar-se de prononomes, ou outro tipo de palavras que não são do interesse do problema, pelo que devem ser ignorados.

- O primeiro método implementado foi a remoção de linhas que indicavam a página do livro, uma vez que estas possuem um padrão com nomes detetados, não sendo parte do problema em estudo.

- Outro método implementado foi a remoção de entradas no dicionário com um valor de interações menor do que um determinado _threshold_ fornecido como argumento da função. Assim, foi possível remover entradas com pouca informação, sendo que, na maioria das vezes, se tratavam de erros.

- Além dos mencionados, no momento da realização de combinações, são removidas entradas que pertençam a uma lista com valores previamente definidos como erros, tais como __I__, __There__ ou __Why__.

- É, também, importante mencionar que por questões associadas ao problema, existe uma remoção de relações de uma entidade consigo própria, antes da atualização da estrutura que trata de manter esta contagem. No mesmo seguimento desta funcionalidade, teve que ser tratado o caso em que se geravam dois pares distintos para uma mesma relação, como: __{Harry}{Ron}__ e __{Ron}{Harry}__. A resolução deste problema foi bastante simples, tirando-se proveito de um método combinatório. Assim, é possível só relacionar os elementos uma vez por frase, pelo que bastou ordenar os pares alfabeticamente antes da atualização do seu número de interações. 

### Interpretador

- Outro requisito apresentado pelo docente passava por permitir que o utilizador indicasse uma personagem, sendo que deveriam ser apresentadas as restantes personagens com as quais a primeira interagiu. Para tal, tendo em conta que se trata de uma fase em que o grafo já está completamente construído, apenas é necessário retornar os vizinhos do nodo. Caso a personagem não exista no grafo, é retornada uma lista vazia e uma mensagem a indicar a não existência da personagem.
    
### Representar graficamente 

- Por fim, o requisito opcional do projeto passava pela representação gráfica da estrutura desenvolvida, de modo a permitir a simples visualização dos relacionamentos entre personagens. De modo a simplificar a visualização, o exemplo apresentado em seguida teve uma remoção de nodos com um _threshold_ de 12 unidades. A ideia passou por converter o grafo original para um grafo no formato de _graphviz_, sendo associado um peso a cada ligação, o qual representa o valor de interações entre os nodos.  

<img src="https://github.com/citoplasme/SPLN_Projetos/blob/master/TP1/output/grafo.png" alt="Grafo com nodos com mais de 12 interações" width="600"/>

## Como utilizar

O programa recebe como argumento o ficheiro a analisar, no formato:

```sh
python3 projeto.py ficheiro
```

Após o _print_ do grafo em formato textual no _stdout_, o programa fica à espera de nomes de personagens para calcular as suas interações, na forma:

```sh
Crabbe
['{Malfoy}', '{Goyle}']
```
De modo a finalizar a execução deste ciclo, o utilizador apenas tem que escrever _quit_ no _stdin_.  

A representação gráfica do grafo é colocada na forma de ficheiro na diretoria __output__ sobre o nome __grafo.png__.

Por fim, note-se que é necessário ter o _graphviz_ instalado na máquina, bem como as bibliotecas apresentadas em seguida:

```python
import fileinput
import re
import itertools
import matplotlib.pyplot as plt
import networkx as nx
import sys
import pygraphviz as pgv
```

&nbsp;

&nbsp;

*Projeto Universitário - Scripting no Processamento de Linguagem Natural, Universidade do Minho (2019-2020)*

