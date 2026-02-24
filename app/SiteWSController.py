from fastapi import WebSocket, WebSocketDisconnect
from app.RoomWSController import RoomWSController, RoomListener


class SiteWSController(RoomListener):
    roomsController: RoomWSController
    sockets: list[WebSocket] = []

    def __init__(self, roomsController):
        self.roomsController = roomsController

    def prepare_json_data(self):
        return list(map(lambda room: {
            "id": room.id,
            "players_count": len(room.sockets)
        }, self.roomsController.rooms))

    async def update(self):
        data = self.prepare_json_data()
        for socket in self.sockets:
            await socket.send_json(data)

    async def controller(self, websocket: WebSocket):
        await websocket.accept()
        self.sockets.append(websocket)

        try:
            data = self.prepare_json_data()
            await websocket.send_json(data)
            while True:
                await websocket.receive_text()
        except WebSocketDisconnect:
            self.sockets.remove(websocket)
