import threading
import time

from fastapi import APIRouter, Query, Request
from fastapi.responses import JSONResponse
from sse_starlette import EventSourceResponse
event_stream_router = APIRouter()

ONLINE_CLIENTS = {}                 # Lista de clientes online
CLIENTS_LOCK = threading.Lock()     # Mutex para não virar bagunça

# Lida com a conexão do cliente
def handle_client_connection(nickname: str, client: Request):

    if nickname in ONLINE_CLIENTS:
        del ONLINE_CLIENTS[nickname]

    print(f'👏 Client connected -> {nickname}')   # Log de conexão com o client
    ONLINE_CLIENTS[nickname] = client             # Adiciona cliente na lista de Clientes Online

    try:
        #while not await client._is_disconnected():
        while True:
            ...

    finally:
        print(f'💨 Client disconnected -> {nickname}')
        del ONLINE_CLIENTS[nickname]  # Remove o cliente da lista de Clientes Online

# Lida com o envio de mensagens
def handle_send_messages(nickname):
    while nickname in ONLINE_CLIENTS:
        yield f'data: Estamos online, {nickname}\n\n'
            
        time.sleep(1)  # Emitindo eventos a cada 1 segundo

@event_stream_router.get('/event-stream')
async def event_stream_endpoint(request: Request, nickname: str = Query()): 
    try:
        threading.Thread(
            target=handle_client_connection,
            args=(nickname, request),
            daemon=True
        ).start()

        return EventSourceResponse(handle_send_messages(nickname), media_type='text/event-stream')

    except Exception as error:
        print(error)
        return JSONResponse(status_code=500, content={'message': 'Internal server error.'})