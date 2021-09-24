# Detecção de falha em equipamentos rotativos através de análise de vibração utilizando Redes Neurais

#### Aluno: [Diogo Ventura Nomiya](https://github.com/diogovn)
#### Orientadora: [Manoela Kohler](https://github.com/manoelakohler)

---

Trabalho apresentado ao curso [BI MASTER](https://ica.puc-rio.ai/bi-master) como pré-requisito para conclusão de curso e obtenção de crédito na disciplina "Projetos de Sistemas Inteligentes de Apoio à Decisão".

- [ProjetoVibracaoBI.ipynb](ProjetoVibracaoBI.ipynb) : arquivo principal - treinamento dos modelos.

- [Leitura.py](Leitura.py) : auxiliar - letura dos dados.
---

### Resumo

Equipamentos rotativos de grande porte freqüentemente têm sua condição monitorada através de diversas técnicas, sendo uma das mais importantes a análise de vibração. Nesta técnica, o equipamento tem sua vibração medida em diversos pontos de medição e analisada periodicamente, buscando detectar falhas ainda em estado incipiente, levando a uma economia de tempo e dinheiro.

Este trabalho tem como objetivo o desenvolvimento de uma ferramenta que auxilie a tomada de decisão do especialista que analisa a vibração de conjuntos moto-bombas. A ferramenta proposta utiliza como entrada os sinais de vibração radial (eixos horizontal e vertical) medidos em 4 pontos distintos do equipamento, totalizando 8 sinais de vibração - todos passados para o domínio da freqüência ("spectro de freqüência").

Os sinais medidos foram utilizados no treinamento de redes neurais, que classificam a condição do equipamento como "normal" ou "crítica". Neste trabalho foram utilizados os modelos dense e CNN/dense. Foram treinados separadamente modelos utilizando sinais de aceleração ou envelope. 

### 1. Introdução

A análise de vibração é uma técnica comumente usada para monitorar a condição de equipamentos rotativos. Para realizar as medições dos sinais de vibração, os equipamentos podem possuir sensores instalados, permitindo o monitoramento contínuo, ou podem ser utilizados sensores portáteis que necessitam de mão-de-obra humana para sua operação, neste caso o monitoramento é feito de forma periódica. Neste trabalho, as medições foram coletadas através de sensores portáteis, em períodos que geralmente variam em torno de 1 e 6 meses.

As medições podem ser coletadas em diversas posições (pontos de medição) do equipamento. Aqui foram consideradas as medições radiais tomadas no eixos horizontal e vertical de 4 posições, desta forma, os 8 pontos de medição considerados foram:
![Pontos de medição de vibração no conjunto moto-bomba. À esquerda, o motor, e à direita, a bomba.](https://github.com/diogovn/BI-Master/blob/main/pontos_medicao.png)
1H) Mancal lado não acoplado do motor - horizontal
1V) Mancal lado não acoplado do motor - vertical
2H) Mancal lado  acoplado do motor - horizontal
2V) Mancal lado  acoplado do motor - vertical
3H) Mancal lado acoplado da bomba - horizontal
3V) Mancal lado acoplado da bomba - vertical
4H) Mancal lado não acoplado da bomba - horizontal
4V) Mancal lado não acoplado da bomba - vertical

Os sinais de vibração são coletados num breve período de tempo e então são passados para o domínio da freqüência, através da tranformada de Fourier. Neste trabalho não foram utilizados os sinais no domínio do tempo, apenas no domínio da freqüência ("spectro" de freqüência). Os sinais também podem ser do tipo envelope, velocidade ou aceleração. Aqui foram considerados sinais de envelope (sinais de 801 amostras) e de aceleração (sinais de 401 amostras).

### 2. Modelagem

Para monitorar a condição do equipamento, o especialista analisa as medições de vibração coletadas nos 8 pontos de medição daquele equipamento em uma determinada data. De acordo com as características desses sinais, é emitido um relatório indicando se o equipamento está normal ou em situação crítica. Para este trabalho, foram considerados 282 relatórios de 18 equipamentos diferentes.

Sendo assim, a base de dados associa uma condição (normal ou crítica) a cada conjunto de medições de vibração (uma para cada um dos 8 pontos de medição) numa mesma data, isto é, os dados de entrada possuem dimensão 8 x 401 (aceleração) ou 8 x 801 (envelope). Vale ressaltar que todos os equipamentos operam na mesma faixa de rotação (3600 rpm) e o eixo-x do gráfico de vibração é exatamente igual para todos os equipamentos, portanto foi descartado e considerado apenas o eixo-y. A saída é um único valor (0-normal e 1-crítico). Como a quantidade de relatórios em situação normal (205) era bem maior do que os críticos (77), foi realizado um random oversampling dos dados críticos.

Esses dados foram utilizados para treinar redes neurais do tipo dense (fully connected) e convolucionais-dense (CNN-dense). Para os modelos dense, foi utilizada uma camada do tipo Flatten como primeira camada, para trazer os dados de entrada para uma única dimensão. Na seqüência, foram utilizadas duas camadas dense: uma de 300 e outra de 50 neurônios, ambas com função de ativação ReLu. A saída é uma camada de 1 único neurônio e função sigmoidal, dado que é um valor binário.

Já os modelos CNN-dense, foram compostos de uma camada convolucional de 30 filtros de tamanho 1x5, uma camada de batch normalization e uma camada de MaxPool, seguidas do mesmo formato da rede tipo dense (Flatten e 3 camadas de 300, 50 e 1 neurônio, nessa ordem).

No código disponibilizado, foi criado um objeto para realizar a leitura dos dados para treinamento. Em uma instância foram armazenados os dados dos sinais de velocidade e na outra os sinais de envelope. Para cada um dos 2 tipos de sinal, foram gerados modelos de redes neurais tipo dense e CNN-dense. Para todos os treinamentos, foram separados 20% dos dados para validação.


### 3. Resultados

Os modelos foram treinados para 100 épocas de treinamento e em lotes (batch_size) de 15. A eficácia na validação geralmente convergia até a vigésima iteração, terminando acima de 90%.

Os valores exatos de eficácia obtidos são mostrados abaixo:

- Sinais de aceleração (401 pontos):
    - CNN-dense:
Eficácia: 95,12% 
Matriz de confusão:
$$
\begin{bmatrix}
42 & 4\\ 
0 & 36\\
\end{bmatrix}
$$

    - Dense:
Eficácia: 95,12% 
Matriz de confusão:
$$
\begin{bmatrix}
42 & 4\\ 
0 & 36\\
\end{bmatrix}
$$

- Sinais de envelope (801 pontos):
    - CNN-dense:
Eficácia: 93,90% 
Matriz de confusão: 
$$
\begin{bmatrix}
41 & 5\\ 
0 & 36\\
\end{bmatrix}
$$

    - Dense:
Eficácia: 91,46% 
Matriz de confusão: 
$$
\begin{bmatrix}
39 & 7\\ 
0 & 36\\
\end{bmatrix}
$$

### 4. Conclusões

Neste trabalho foi desenvolvida um ferramenta para auxiliar o especialista durante uma análise de vibração. Foram treinados modelos para identificar se a condição do equipamento está em estado normal ou crítico.

Pelos resultados obtidos, é possível notar que a eficácia se mostra um melhor quando foram utilizados os sinais de aceleração. Neste caso, tanto o modelo CNN-dense quanto o dense apresentaram o mesmo valor de eficácia. Com os sinais de envelope, o modelo CNN-dense apresentou resultados superiores ao modelo dense.

Quando analisamos as matrizes de confusão, notamos que todos as previsões incorretas foram falso-negativo, isto é, equipamentos que estariam com a condição normal foram classificados como críticos. Neste caso, todos os erros levariam a um estado mais conservador, dado que uma indicação de estado crítico levaria o especialista a analisar o equipamento com mais cautela.

Como trabalho futuro, pode-se considerar o treinamento dos modelos com ainda mais dados, para buscar mais robustez. Outro ponto de melhoria seria incluir o eixo-x dos gráficos de vibração, para possibilitar o treinamento de modelos a partir equipamentos de diferentes rotações, visando trazer mais flexibilidade.

---

Matrícula: 192.671.098

Pontifícia Universidade Católica do Rio de Janeiro

Curso de Pós Graduação *Business Intelligence Master*
