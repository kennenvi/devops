from fastapi import FastAPI

from datetime import datetime


APP_NOTIFICACAO = FastAPI()

NOTIFICACOES = []


@APP_NOTIFICACAO.get("/")
def index():
    global NOTIFICACOES
    return NOTIFICACOES

@APP_NOTIFICACAO.post('/notificar')
def notificar(titulo: str, data_finalizacao: datetime):
    global NOTIFICACOES

    mensagem = f'titulo {titulo}, data de finalização: {data_finalizacao}'
    print(mensagem)
    NOTIFICACOES.append(mensagem)
    
    return {'mensagem': 'Mensagem recebida'}