from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware

from app.SiteWSController import SiteWSController
from app.RoomWSController import RoomWSController

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

roomController = RoomWSController()
siteController = SiteWSController(roomController)

roomController.add_listener(siteController)


@app.websocket('/ws')
async def siteWS(websocket: WebSocket):
    return await siteController.controller(websocket)


@app.websocket('/ws/{room_id}')
async def roomWS(room_id, websocket: WebSocket):
    return await roomController.controller(room_id, websocket)


@app.get('/create_room')
async def create_room():
    id = await roomController.create_room()
    return id
