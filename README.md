
#  Projeto Integrador I
### Univesp - 03/2021 - SCS
Repositório destinado para o projeto integrador I de Computação da Univesp. Cujo grupo é formado por integrantes do Campus SCS.


## Passo a passo

### Github
#### Como acessar os arquivos via Github
1. Criar conta no Github
2. Baixar e instalar o Github na máquina: https://desktop.Github.com/
3. Configurar o Github na máquina [1]
   - Verificar sua conta do Github
   - Clique em sua foto de perfil e abra configurações.
   - Clique em Developer settings
   - Clique em tokens de acesso pessoal.
   - Gere um token, clique em Generate new token .
   - De um nome para o token.
   - Selecione os escopos que contém nome repo.
   - Clique em Generate Token.
   - Agora copie seu token e execute os próximos comandos no terminal:
   
   ```
   git config --global user.name "seu username"
   git config --global user.password "token gerado"
   ```

4. Clonar o repositório [2]:

    `git clone https://Github.com/iurizambotto/projeto-integrador-I.git`
    
    OU
    
    "OPEN WITH Github DESKTOP" 
    ![image](https://user-images.githubusercontent.com/51412949/139102667-9cde37ef-43d6-455b-a54d-7ec8dba7078c.png)
   
5. Verifique se as pastas/arquivos do repositório estão na sua máquina e pronto.


#### Como usar o Github
##### Pull
O comando pull é utilizado para PUXAR/TRAZER os dados que estão no repositório para a sua máquina:
`git pull origin main`

##### Branches
As branches (ramos) são as diferentes RAMIFICAÇÕES que um repositório tem. Por exemplo, por padrão todos repositório contém PELO MENOS uma branch, no nosso caso, é a branch MAIN, ou seja, a branch principal que conterá os códigos da aplicação.
Porém quando usamos ramificações, podemos fazer ALTERAÇÕES no código SEM IMPACTAR na branch principal, ou seja, caso as alterações estejam corretas, nós iremos MERGEAR a branch que foi alterada para a branch main.

O ideal aqui, seria cada um de nós ter sua própria branch, e para criar uma branch, execute o comando:
`git checkout -b nome_da_sua_branch`

Executando este comando você já estará nesta sua branch nova.

##### Commits
Após fazer algumas alterações no código da sua branch, você precisará COMMITAR, ou seja, ENVIAR esses dados para o repositório do Github, para isso, use:
`git commit -m "digite aqui o resumo das suas alteracoes"`

##### Push

##### Pull requests (PR)

## Estrutura da aplicação
### Estrutura dos diretórios

#### blueprint
Nesta pasta encontram-se os arquivos PYTHON que definirão as ROTAS da API, ou seja, as views no sistema MVC.

Atualmente só temos UM ARQUIVO de view, e neste arquivo temos muitas LÓGICAS DE NEGÓCIO, uma das tarefas que temos é retirar os códigos que contém lógicas de negócio e mover para a pasta de CONTROLLERs.

#### controllers
Aqui deveriam estar os ARQUIVOS PYTHON referente às lógicas de negócio, ou seja, todo o CRUD (create, read, update e delete) de usuários, atividades e meta deveria estar nessa pasta. Por isso precisamos pegar as funções que estão em views.py e transferir para cá para seu devido arquivo.

#### extensions
Nesta pasta estão arquivos PADRÃO da aplicação, alguns deles são EXTENSÕES, como por exemplo o que define o BANCO DE DADOS (database.py)

#### forms
Todos formulários que forem criados na aplicação - por exemplo, o de LOGIN - deverá ter um arquivo .PY nesta pasta. E nele será definido uma classe do WTForms com seus respectivos campos e tipos.

#### models
Aqui estão definidos os MODELOS DE DADOS, como estamos utilizando o SQL Alchemy, o Flask oferece uma abordagem para facilitar a criação das tabelas e do banco de dados como um todo.

Então aqui definimos as tabelas existentes, com seus respectivos campos e relacionamentos.

#### static
Esta pasta é um diretório padrão para os arquivos de ESTILO (css), ou seja, toda estética da nossa aplicação será definida nessa pasta.

#### templates
Aqui estarão os arquivos .HTML, ou seja, os principais arquivos para uma aplicação web.

Com o Flask, podemos criar um ARQUIVO BASE, e extender os próximos com base neste primeiro.

### Desenho da arquitetura

### Diagrama de Entidade e Relacionamento (DER)





FONTES:

[1] https://digitalinnovation.one/artigos/como-fazer-login-corretamente-no-github-pelo-terminal

[2] https://docs.github.com/pt/github-ae@latest/repositories/creating-and-managing-repositories/cloning-a-repository

[3] https://mbeck.com.br/blog/info/tecnologia/estruturando-aplicacoes-maiores-microframework-flask
