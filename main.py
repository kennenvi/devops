from datetime import datetime

from fastapi import FastAPI


LISTA_TAREFAS = []
APP = FastAPI()

def nova_tarefa(id: int, titulo: str, descricao: str):
    """Função auxiliar para criar uma tarefa usando dicionário (`dict`)"""
    return {
        "id": id,
        "titulo": titulo,
        "descricao": descricao,
        "concluido": False,
        "criado_em": datetime.now()
    }

@APP.get("/")
def index():
    return "Olá, DevOps!"

@APP.get("/tarefas")
def listat_tarefas():
    global LISTA_TAREFAS

    # Lista tarefas (somente id e titulo)
    if len(LISTA_TAREFAS) == 0:
        return LISTA_TAREFAS
    
    return [{"id": tarefa['id'], "titulo": tarefa['titulo']} for tarefa in LISTA_TAREFAS]

@APP.get("/tarefas/{id}")
def listar_tarefa_especifica(id: int):
    global LISTA_TAREFAS
    LISTA_TAREFAS.append(nova_tarefa(0, "nova tarefa", "descricao nova tarefa"))
    mensagem_padrao = {"mensagem": "Não existe nenhuma tarefa"}

    # Lista tarefas (somente id e titulo)
    if len(LISTA_TAREFAS) == 0:
        return mensagem_padrao    

    # ID da tarefa é o índice da lista
    if id >= 0 and id < len(LISTA_TAREFAS):
        return LISTA_TAREFAS[id]
    else:
        return mensagem_padrao
