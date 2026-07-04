from app import APP

from fastapi.testclient import TestClient

CLIENT = TestClient(APP)


def test_index():
    requisicao = CLIENT.get('/')

    assert requisicao.status_code == 200
    assert requisicao.json() == "Olá, DevOps!"


# Criar um teste unitário para validar se a tarefa foi criada com sucesso
# CLIENT.post(...) (substituir pela string para criação de tarefa)
# Verificar se o código de status é 200
# Verificar se o retorno, quando tarefa é criada, é igual a {"mensagem": "OK"} ou conforme definido na sua API
# Verificar se o retorno, quando a tarefa já existe, é igual a {"mensagem" : "TAREFA JÁ EXISTE"} ou conforme definido na sua API
def test_criacao_tarefa():
    args = 'id=0&titulo=teste&descricao=teste'

    requisicao = CLIENT.post(f'/tarefas?{args}')
    print(requisicao)

    assert requisicao.status_code == 201
    assert requisicao.json() == {'mensagem': 'tarefa criada'}

def test_cricao_tarefa_ja_existe():
    args = 'id=0&titulo=teste&descricao=teste'

    requisicao = CLIENT.post(f'/tarefas?{args}')
    print(requisicao.status_code)
    requisicao_erro = CLIENT.post(f'/tarefas?{args}')

    assert requisicao_erro.status_code == 409
    assert requisicao_erro.json()['detail'] == "Tarefa já existe"