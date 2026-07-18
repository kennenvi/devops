# Descrição

Este projeto foi desenvolvido como parte das atividades práticas do curso de **DevOps**, com o objetivo de aplicar os principais conceitos relacionados ao desenvolvimento, integração contínua, segurança, conteinerização e implantação automatizada de aplicações.

A aplicação consiste em uma **API REST** desenvolvida com **FastAPI**, contemplando desde a implementação e testes automatizados até a construção de um pipeline completo de **CI/CD**.

Durante o desenvolvimento foram implementadas as seguintes etapas:

* Desenvolvimento de uma API REST utilizando **FastAPI**;
* Criação e execução de testes automatizados;
* Integração contínua (CI) utilizando **GitHub Actions**;
* Verificação de conformidade de licenças utilizando **FOSSA**;
* Construção automatizada de imagens **Docker**;
* Publicação das imagens no **Docker Hub**;
* Deploy automatizado utilizando **GitHub Actions Runner** em um ambiente **Kubernetes**.

## Como utilizar

### Executando localmente

Para executar a aplicação localmente, é necessário ter o **Python** instalado e criar um ambiente virtual para instalar as dependências do projeto.

```bash
python3 -m venv devops
source devops/bin/activate
pip install -r requirements.txt
```

Após a instalação das dependências, inicie a API desejada.

#### API de Tarefas

```bash
fastapi dev app/ --host 0.0.0.0
```

#### API de Notificação

```bash
fastapi dev -e app.notificacao:APP_NOTIFICACAO --host 0.0.0.0
```

---

### Executando com Docker Compose

Também é possível executar toda a aplicação utilizando o Docker Compose. Esse comando iniciará:

* API de Tarefas;
* API de Notificação;
* API Gateway utilizando **Nginx**.

```bash
docker compose up --build -d
```

Após a inicialização, as APIs estarão disponíveis nos seguintes endpoints:

* API de Tarefas: `http://localhost/tarefas`
* API de Notificação: `http://localhost/notificar`

---

## Pipeline CI/CD

A pipeline é executada automaticamente sempre que um **Pull Request** é aberto para a branch `main`.

Ela é composta pelas seguintes etapas:

### Análise de dependências e licenças

Nesta etapa é realizada a análise de dependências (**SCA**) e a verificação de conformidade de licenças utilizando o **FOSSA**.

Para sua execução, é necessário:

* Configurar a variável `FOSSA_API_KEY` nos **GitHub Secrets**;
* Disponibilizar um **GitHub Self-Hosted Runner**, responsável pela execução desta etapa.

### Build e publicação da imagem Docker

A etapa de entrega realiza a construção da imagem Docker e sua publicação no **Docker Hub**.

Para isso, configure:

* `DOCKERHUB_TOKEN` nos **GitHub Secrets**;
* `DOCKERHUB_USERNAME` nas **GitHub Actions Variables**.

### Deploy

O deploy é realizado automaticamente utilizando um **GitHub Self-Hosted Runner**, que aplica as alterações no cluster **Kubernetes**.

Para acessar a aplicação após a implantação, execute:

```bash
kubectl port-forward --address 0.0.0.0 svc/devops-svc 8889:8000
```

A aplicação ficará disponível em:

```text
http://localhost:8889
```

## Tecnologias Utilizadas

* **Python**
* **FastAPI**
* **Pytest**
* **PyLint**
* **Bandit**
* **GitHub Actions**
* **FOSSA**
* **Docker**
* **Kubernetes**
* **Git**
