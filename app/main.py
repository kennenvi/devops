from datetime import datetime, timedelta
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

#   - Quantidade total de tarefas
#   - Quantidade de tarefas pendentes
#   - Quantidade de tarefas concluídas
#   - Quantidade de tarefas atualizadas
#   - Quantidade de tarefas removidas
#   - Tempo médio para conclusão de tarefa

METRICAS = {
    'qtde_tarefas': 0,
    'qtde_tarefas_pendentes': 0,
    'qtde_tarefas_concluidas': 0,
    'qtde_tarefas_atualizadas': 0,
    'qtde_tarefas_removidas': 0,
    'tempo_medio_conclusao_tafefa': 0,
}


def nova_tarefa(id: int, titulo: str, descricao: str):
    """Função auxiliar para criar uma tarefa usando dicionário (`dict`)"""
    tarefa = {
        "id": id,
        "titulo": titulo,
        "descricao": descricao,
        "concluido": False,
        "criado_em": datetime.now()
    }
    LOGGER.debug(f'Tarefa criada: {str(tarefa)}')
    return tarefa

def verifica_tarefa_existente(id: int) -> bool:
    for tarefa in LISTA_TAREFAS:
        if tarefa['id'] == id:
            return True
    return False

def encontra_tarefa_index(id: int) -> int | None:
    for i, cur_tarefa in enumerate(LISTA_TAREFAS):
        if cur_tarefa['id'] == id:
            return i
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
    
    tarefas = []

    for tarefa in LISTA_TAREFAS:
        info = {"id": tarefa['id'], "titulo": tarefa['titulo']}
        tarefas.append(info)
    
    return tarefas

@APP.get("/tarefas/{id}")
def listar_tarefa_especifica(id: int):
    LOGGER.info("Acesso a rota listar_tarefa_especifica")
    global LISTA_TAREFAS

    # Lista tarefas (somente id e titulo)
    if len(LISTA_TAREFAS) == 0:
        return {"mensagem": "Não existe nenhuma tarefa"}    

    # ID da tarefa é o índice da lista
    if id >= 0 and id < len(LISTA_TAREFAS):
        LOGGER.info(f"Acesso a rota listar_tarefa_especifica /tarefa/{id}")
        return LISTA_TAREFAS[id]
    else:
        return {'mensagem': 'Tarefa não existe'}

# Implementar
@APP.post("/tarefas", status_code=201)
def criar_tarefa(id: int, titulo: str, descricao: str):
    global LISTA_TAREFAS, METRICAS

    if verifica_tarefa_existente(id):
        LOGGER.error(f"Tarefa id={id}, já existe")
        raise HTTPException(status_code=409, detail="Tarefa já existe")
    
    nova = nova_tarefa(id, titulo, descricao)
    LISTA_TAREFAS.append(nova)
    LOGGER.info(f"Acesso a rota criar_tarefa com tarefa id={id}")

    METRICAS['qtde_tarefas'] += 1

    return {'mensagem': 'tarefa criada'}

@APP.put("/tarefas/{id}")
def atualizar_tarefa(
        id: int, 
        titulo: str | None = None, 
        descricao: str | None = None, 
        concluido: bool | None = None
    ):
    global LISTA_TAREFAS, METRICAS
    
    if not verifica_tarefa_existente(id):
        LOGGER.error(f"Tarefa id={id}, não existe")
        return {"mensagem": "Tarefa não existe"}

    tarefa_index = encontra_tarefa_index(id)
    print(tarefa_index)
    tarefa = LISTA_TAREFAS[tarefa_index]
    
    if titulo:
        tarefa['titulo'] = titulo
    if descricao:
        tarefa['descricao'] = descricao
    if concluido:
        tarefa['concluido'] = concluido
    
    if concluido == True:
        METRICAS['qtde_tarefas_concluidas'] += 1
        LISTA_TAREFAS[tarefa_index]['concluido_em'] = datetime.now()
        # requests.post(f'http://svc-notificacao.svc./notificar?titulo={tarefa["titulo"]}&data_finalizacao={datetime.now()}',
        #               timeout=30)
    
    LISTA_TAREFAS[tarefa_index]['concluido'] = concluido

    LOGGER.debug(f"Tarefa atualizada = {LISTA_TAREFAS[tarefa_index]}")
    LOGGER.info(f"Rota PUT '/tarefas/{id}' acessada. Tarefa id={id} atualizada.")

    METRICAS['qtde_tarefas_atualizadas'] += 1
    METRICAS['qtde_tarefas_pendentes'] = METRICAS['qtde_tarefas'] - METRICAS['qtde_tarefas_concluidas']

    return {'mensagem': 'Tarefa atualizada'}

@APP.delete("/tarefas/{id}")
def excluir_tarefa(id: int):
    LOGGER.info("Acesso a rota excluir_tarefa")
    global LISTA_TAREFAS, METRICAS
    
    if not verifica_tarefa_existente(id):
        LOGGER.error(f"Tarefa id={id}, não existe")
        return {"mensagem": "Tarefa não existe"}
    
    tarefa_index = encontra_tarefa_index(id)
    LOGGER.info(f'id={id}')
    LOGGER.info(f'tarefa={tarefa_index}')
    LOGGER.info(f'lista_tarefas={LISTA_TAREFAS}')
    del LISTA_TAREFAS[tarefa_index]

    LOGGER.info(f"Rota DELETE '/tarefas/{id}' acessada. Tarefa id={id} removida.")

    METRICAS['qtde_tarefas_removidas'] += 1
    METRICAS['qtde_tarefas'] -= 1

    return {"mensagem": "Tarefa excluída"}

@APP.get('/health')
def health():
    LOGGER.info("Acesso a rota health")
    return {"status": "OK"}

@APP.get('/metricas')
def metricas():
    
    tempo_medio_total = timedelta()
    
    for tarefa in LISTA_TAREFAS:
        if tarefa['concluido']:
            tempo_medio = tarefa['concluido_em'] - tarefa['criado_em']
            tempo_medio_total += tempo_medio

    if METRICAS['qtde_tarefas_concluidas'] > 0:
        METRICAS['tempo_medio_conclusao_tarefa'] = tempo_medio_total / METRICAS['qtde_tarefas_concluidas']
    
    LOGGER.debug(METRICAS)
    LOGGER.info("Rota '/metricas' acessada.")

    return METRICAS
