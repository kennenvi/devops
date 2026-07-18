from fastapi.testclient import TestClient

from app import APP
from tests.test_main import criar_tarefa_mock

CLIENT = TestClient(APP)

def test_qtde_tarefas():
    criar_tarefa_mock(id=0)

    requisicao = CLIENT.get("/metricas").json()
    print(requisicao)

    assert requisicao['qtde_tarefas'] == 1

def test_qtde_tarefas_concluidas():
    CLIENT.put("/tarefas/0?concluido=true")

    requisicao = CLIENT.get("/metricas").json()

    assert requisicao['qtde_tarefas_concluidas'] == 1
    assert requisicao['qtde_tarefas_pendentes'] == 0
    assert requisicao['qtde_tarefas_atualizadas'] == 2


def test_apagar_tarefa():
    CLIENT.delete("/tarefas/0")

    requisicao = CLIENT.get("/metricas").json()

    assert requisicao['qtde_tarefas_removidas'] == 5
    assert requisicao['qtde_tarefas'] == 0

 
 