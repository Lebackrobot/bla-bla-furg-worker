from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.endpoints.event_stream_router import event_stream_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

app.include_router(event_stream_router)
