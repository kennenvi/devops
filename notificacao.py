from fastapi import FastAPI

from datetime import datetime


APP_NOTIFICACAO = FastAPI()


@APP_NOTIFICACAO.get("/")
def index():
    return 'Olá, notificação'

@APP_NOTIFICACAO.post('/notificar/')
def notificar(titulo: str, data_finalizacao: datetime):
    mensagem = f'titulo {titulo}, data de finalização: {data_finalizacao}'
    print(mensagem)
    return {'mensagem': mensagem}