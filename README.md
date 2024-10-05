# b3loader
Conjunto com os principais códigos para carga de dados do mercado a vista B3.

## Este projeto possui quatro partes que rodam cada uma em um dos meus raspberrypis mas que formam um ciclo virtuoso para inteligência de trade, são elas: 

**1. B3Springboot** - roda como um microservico java springboot em algum nó do cluster de raspberrypis, atua  como uma interface para a base mongodb cotendo a lista de ativos “foco”; 
<br>Possui dois serviços:  <br>
    &nbsp;&nbsp;&nbsp;&nbsp;1. registerb3asset - Registro da lista de Ativos Selecionados;<br>
    &nbsp;&nbsp;&nbsp;&nbsp;2. b3assets - Lista os Ativos Selecionados;<br><br>
    
**2. B3Metatrader** - script python que roda agendado diariamente em máquina windows com Metatrader instalado, possui dois módulos:<br>
    &nbsp;&nbsp;&nbsp;&nbsp;1. SelectData - Seleciona dentre todos os ativos da B3 somente os do mercado a vista e com volume diário acima de R$ 5milhóes; - invoca o registerb3assets para registrar os ativos selecionados;<br>
    &nbsp;&nbsp;&nbsp;&nbsp;2. LoadData - Obtém os dados dos ativos selecionados e de forma incremental armazena os dados em arquivo texto (inicia-se a partir de lista obtida de b3assets);<br><br>
**3. B3HadoopSpark** - scripts de dados no formato de notebooks que rodam no Jupyter Notebook instanciando executores spark do cluster que rodo aqui nos meus raspberrypi e que estruturam os dados obtidos a partir do metatrader;<br><br>
**4. B3MLOps** - Há ainda um último módulo que utiliza os dados estruturados: calcula indices, aplica algoritmos do Machine Learning e armazena as predições em base mongo;<br><br>
5.  E ainda, para fechar o ciclo adiciona-se:<br>
    &nbsp;&nbsp;&nbsp;&nbsp;1. um serviço (predict) no mesmo B3SpringBoot acima para leitura da base mongo contendo as predições;<Br>
    &nbsp;&nbsp;&nbsp;&nbsp;2. Script mql5 que roda em tempo real no MetaTrader e que aciona a execução de ordens automáticas a partir dos dados das predições feitas pelo B3MLOPs acima invocando o serviço “predict”acima;<br>
    &nbsp;&nbsp;&nbsp;&nbsp;3. Para controle do portfolio e retroalimentação do algorítmo de predição há ainda os serviços para registro dos dados de cada ordem feita no mesmo B3SpringBoot;
<br>
<br>
### Para esta publicação, somente os módulos B3SpringBoot (sem os serviços adicionais de predição e de registro de ordens), B3MetaTrader e B3HadoopSpark é que farão parte.


