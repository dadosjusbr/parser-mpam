# Ministério Público do Estado do Amazonas (MPAM)

Este coletor tem como objetivo a recuperação de informações sobre folhas de pagamentos de funcionários a partir do Ministério Público do Estado do Amazonas. O site com as informações pode ser acessado [aqui](https://www.mpam.mp.br/servicos/transparencia-novo).

## Como usar
### Executando com Docker

 - Inicialmente é preciso instalar o [Docker](https://docs.docker.com/install/). 

 - Construção da imagem:

    ```sh
    $ cd coletores/mpam
    $ sudo docker build -t mpam .
    ```
 - Execução:
 
    ```sh
    $ sudo docker run -e YEAR=2018 -e MONTH=01 -e GIT_COMMIT=$(git rev-list -1 HEAD) mpam
    ```
### Execução sem o Docker:

- Para executar o script é necessário rodar o seguinte comando, a partir do diretório `/mpam`, adicionando às variáveis seus respectivos valores, a depender da consulta desejada. É válido lembrar que faz-se necessario ter o [Python 3.6.9](https://www.python.org/downloads/) instalado.

    ```sh
    MONTH=01 YEAR=2018 GIT_COMMIT=$(git rev-list -1 HEAD) python3 src/main.py
    ```
- Para que a execução do script possa ser corretamente executada é necessário que todos os requirements sejam devidamente instalados. Para isso, executar o [PIP](https://pip.pypa.io/en/stable/installing/) passando o arquivo requirements.txt, por meio do seguinte comando:

   ```sh
   pip install -r requirements.txt
   ```