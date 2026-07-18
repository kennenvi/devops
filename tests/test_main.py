from fastapi.testclient import TestClient
from unittest.mock import patch

from app import APP


CLIENT = TestClient(APP)


def criar_tarefa_mock(id: int = 0, titulo: str = 'titulo_teste', descricao: str = 'descricao_teste') -> None:
    args = f'id={id}&titulo={titulo}&descricao={descricao}'
    CLIENT.post(f'/tarefas?{args}')

def setup_tarefas(quantidade_tarefas=5, qtd_concluida=3):
    for id_tarefa in range(quantidade_tarefas):
        criar_tarefa_mock(id=id_tarefa)
    for id_tarefa in range(qtd_concluida):
        CLIENT.put(f'tarefas/{id_tarefa}?concluido=true')

def test_index():
    requisicao = CLIENT.get('/')

    assert requisicao.status_code == 200
    assert requisicao.json() == "Olá, DevOps!"


# Criar um teste unitário para validar se a tarefa foi criada com sucesso
# CLIENT.post(...) (substituir pela string para criação de tarefa)
# Verificar se o código de status é 200
# Verificar se o retorno, quando tarefa é criada, é igual a {"mensagem": "OK"}
# ou conforme definido na sua API
# Verificar se o retorno, quando a tarefa já existe, é igual a
# {"mensagem" : "TAREFA JÁ EXISTE"} ou conformkkke definido na sua API
def test_criacao_tarefa():
    args = 'id=0&titulo=teste&descricao=teste'

    requisicao = CLIENT.post(f'/tarefas?{args}')
    print(requisicao)

    assert requisicao.status_code == 201
    assert requisicao.json() == {'mensagem': 'tarefa criada'}

def test_cricao_tarefa_ja_existe():
    criar_tarefa_mock()

    args = 'id=0&titulo=teste&descricao=teste'
    requisicao_erro = CLIENT.post(f'/tarefas?{args}')

    assert requisicao_erro.status_code == 409
    assert requisicao_erro.json()['detail'] == "Tarefa já existe"

def test_remover_tarefa():
    criar_tarefa_mock()

    requisicao = CLIENT.delete('/tarefas/0')
    assert requisicao.status_code == 200
    assert requisicao.json() == {"mensagem": "Tarefa excluída"}

    requisicao = CLIENT.delete('tarefas/5')
    assert requisicao.status_code == 200
    assert requisicao.json() == {"mensagem": "Tarefa não existe"}

def test_atualizar_tarefa():
    criar_tarefa_mock()

    args = 'id=0&descricao=descricao_teste&titulo=titulo_teste'
    requisicao = CLIENT.put(f'/tarefas/0?{args}')
    assert requisicao.status_code == 200
    assert requisicao.json() == {'mensagem': 'Tarefa atualizada'}

    requisicao = CLIENT.get('tarefas/0')
    assert requisicao.status_code == 200
    assert requisicao.json()['descricao'] == 'descricao_teste'

def test_busca_tarefa():
    criar_tarefa_mock()

    requisicao = CLIENT.get(f'/tarefas/0')
    assert requisicao.status_code == 200
    dados = requisicao.json() 
    print(dados)

    assert dados['id'] == 0
    assert dados['descricao'] == 'descricao_teste'
    assert dados['titulo'] == 'titulo_teste'
    assert dados['concluido'] == False

    requisicao = CLIENT.get('tarefas/5')
    assert requisicao.status_code == 200
    assert requisicao.json() == {"mensagem": "Tarefa não existe"}

def test_health():
    requisicao = CLIENT.get(f'/health')
    
    assert requisicao.status_code == 200
    assert requisicao.json() == {"status": "OK"}

def test_metrics():
    setup_tarefas(quantidade_tarefas=5, qtd_concluida=3)

    requisicao = CLIENT.get('metrics')

    metrica_esperada = {
        'quantidade_tarefas': 5,
        'tarefas_finalizadas': 3,
        'tarefas_pendentes': 2
    }

    assert requisicao.status_code == 200
    assert requisicao.json() == metrica_esperada
