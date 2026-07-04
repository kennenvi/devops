from datetime import datetime

from fastapi import FastAPI
from fastapi import HTTPException
from pydantic import BaseModel
import requests


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
    return "Olá, DevOps!"

@APP.get("/tarefas")
def listat_tarefas():
    global LISTA_TAREFAS

    # Lista tarefas (somente id e titulo)
    if len(LISTA_TAREFAS) == 0:
        return LISTA_TAREFAS
    
    return LISTA_TAREFAS

@APP.get("/tarefas/{id}")
def listar_tarefa_especifica(id: int):
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
    global LISTA_TAREFAS

    if verifica_tarefa_existente(id):
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
    global LISTA_TAREFAS
    
    if not verifica_tarefa_existente(id):
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
        requests.post(f'http://notificacoes:8000/notificar?titulo={tarefa["titulo"]}&data_finalizacao={datetime.now()}',
                      timeout=30)

    return {'mensagem': 'Tarefa atualizada'}

@APP.delete("/tarefas/{id}")
def excluir_tarefa(id: int):
    global LISTA_TAREFAS
    
    if not verifica_tarefa_existente(id):
        return {"mensagem": "Tarefa não existe"}
    
    tarefa_index = encontra_tarefa_index(id)
    del LISTA_TAREFAS[tarefa_index]

    return {"mensagem": "Tarefa excluída"}

@APP.get('/health')
def health():
    return {"status": "OK"}

@APP.get('/metrics')
def metrics():
    total_tarefas = len(LISTA_TAREFAS)
    tarefas_finalizadas = len([tarefa for tarefa in LISTA_TAREFAS if tarefa['concluido'] == True])
    tarefas_pendentes = len([tarefa for tarefa in LISTA_TAREFAS if tarefa['concluido'] == False])

    metricas = {
        'quantidade_tarefas': total_tarefas,
        'tarefas_finalizadas': tarefas_finalizadas,
        'tarefas_pendentes': tarefas_pendentes
    }

    return metricas


# Criar uma branch nova (git checkout -b <NOME DA BRANCH>)
# -------- OBRIGATÓRIA ---------
# 1. Criar um endpoint /health (GET)
#    1.1 Retornar status_code 200
#    1.2 Retonar {"status": "OK"}
#    1.3 Criar um teste unitário para validar se ambos os pontos 1.1 e 1.2 estão corretos
#    1.4 Commitar alterações e enviar ao repositório (git push -u origin <NOME DA BRANCH>)
#    1.5 Criar pull request
# ------------------------------
# --------- OPCIONAL! ----------
# 2. Criar um endpoint /metricas (GET) (ITEM OPCIONAL!)
#    2.1 Retornar status_code 200
#    2.2 Retonar
#        - Quantidade de tarefas que existem
#        - Quantidade de tarefas finalizadas
#        - Quantidade de tarefas pendentes
#        Exemplo:
#            {"quantidade_tarefas": 3, "tarefas_finalizadas": 2, "tarefas_pendentes": 1}
#    2.3 Criar um teste unitário para validar se ambos os pontos 2.1 e 2.2 estão corretos
#    2.4 Commitar alterações e enviar ao repositório (git push -u origin <NOME DA BRANCH>)
#    2.5 Criar pull request
# ------------------------------
 