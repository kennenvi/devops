from datetime import datetime
import logging
import os

from fastapi import FastAPI
from fastapi import HTTPException
from pydantic import BaseModel
import requests


level = os.environ.get("LOG_LEVEL", logging.INFO)

if level == "DEBUG":
    level = logging.DEBUG
else:
    level = logging.INFO

LISTA_TAREFAS = []
APP = FastAPI()
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(level)

stream_handler  = logging.StreamHandler()
file_handler    = logging.FileHandler("api.log", encoding='utf-8')
fmt             = logging.Formatter(fmt="%(name)s | %(asctime)s | %(levelname)s | %(filename)s:%(lineno)s | %(message)s)")

stream_handler.setFormatter(fmt)
file_handler.setFormatter(fmt)

LOGGER.addHandler(stream_handler)
LOGGER.addHandler(file_handler)

def nova_tarefa(id: int, titulo: str, descricao: str):
    """Função auxiliar para criar uma tarefa usando dicionário (`dict`)"""
    tarefa = {
        "id": id,
        "titulo": titulo,
        "descricao": descricao,
        "concluido": False,
        "criado_em": datetime.now()
    }
    LOGGER.debug(f'Tarefa criada: {tarefa}')
    return tarefa

def verifica_tarefa_existente(id: int) -> bool:
    for tarefa in LISTA_TAREFAS:
        if tarefa['id'] == id:
            return True
    return False

def encontra_tarefa_index(id: int) -> int | None:
    for i, cur_tarefa in enumerate(LISTA_TAREFAS):
        if cur_tarefa['id'] == id:
            tarefa_id = cur_tarefa['id']
            return tarefa_id
    return None

@APP.get("/")
def index():
    LOGGER.info("Acesso o index")
    return "Olá, DevOps!"

@APP.get("/tarefas")
def listat_tarefas():
    LOGGER.info("Acesso a rota listar_tarefas")
    global LISTA_TAREFAS

    # Lista tarefas (somente id e titulo)
    if len(LISTA_TAREFAS) == 0:
        return LISTA_TAREFAS
    
    return LISTA_TAREFAS

@APP.get("/tarefas/{id}")
def listar_tarefa_especifica(id: int):
    LOGGER.info("Acesso a rota listar_tarefa_especifica")
    global LISTA_TAREFAS

    # Lista tarefas (somente id e titulo)
    if len(LISTA_TAREFAS) == 0:
        return {"mensagem": "Não existe nenhuma tarefa"}    

    # ID da tarefa é o índice da lista
    if id >= 0 and id < len(LISTA_TAREFAS):
        return LISTA_TAREFAS[id]
    else:
        return {'mensagem': 'Tarefa não existe'}

# Implementar
@APP.post("/tarefas", status_code=201)
def criar_tarefa(id: int, titulo: str, descricao: str):
    LOGGER.info("Acesso a rota criar_tarefa")
    global LISTA_TAREFAS

    if verifica_tarefa_existente(id):
        LOGGER.error(f"Tarefa id={id}, já existe")
        raise HTTPException(status_code=409, detail="Tarefa já existe")
    
    nova = nova_tarefa(id, titulo, descricao)
    LISTA_TAREFAS.append(nova)

    return {'mensagem': 'tarefa criada'}

@APP.put("/tarefas/{id}")
def atualizar_tarefa(
        id: int, 
        titulo: str | None = None, 
        descricao: str | None = None, 
        concluido: bool | None = None
    ):
    LOGGER.info("Acesso a rota atualizar_tarefa")
    global LISTA_TAREFAS
    
    if not verifica_tarefa_existente(id):
        LOGGER.error(f"Tarefa id={id}, não existe")
        return {"mensagem": "Tarefa não existe"}

    tarefa_index = encontra_tarefa_index(id)
    tarefa = LISTA_TAREFAS[tarefa_index]
    
    if titulo:
        tarefa['titulo'] = titulo
    if descricao:
        tarefa['descricao'] = descricao
    if concluido:
        tarefa['concluido'] = concluido
    
    if concluido == True:
        requests.post(f'http://svc-notificacao.svc./notificar?titulo={tarefa["titulo"]}&data_finalizacao={datetime.now()}',
                      timeout=30)

    return {'mensagem': 'Tarefa atualizada'}

@APP.delete("/tarefas/{id}")
def excluir_tarefa(id: int):
    LOGGER.info("Acesso a rota excluir_tarefa")
    global LISTA_TAREFAS
    
    if not verifica_tarefa_existente(id):
        LOGGER.error(f"Tarefa id={id}, não existe")
        return {"mensagem": "Tarefa não existe"}
    
    tarefa_index = encontra_tarefa_index(id)
    del LISTA_TAREFAS[tarefa_index]

    return {"mensagem": "Tarefa excluída"}

@APP.get('/health')
def health():
    LOGGER.info("Acesso a rota health")
    return {"status": "OK"}