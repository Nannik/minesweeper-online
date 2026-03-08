from fastapi import WebSocket, WebSocketDisconnect
from random import random
from app.Room import Room
from app.Board import GameException
import math


class RoomListener:
    async def update(self):
        pass


class RoomWSController:
    listeners: list[RoomListener] = []
    rooms: list[Room] = []

    def add_listener(self, listener: RoomListener):
        self.listeners.append(listener)

    def get_current_player(self, websocket: WebSocket):
        player = websocket.query_params.get('player')
        if not player:
            websocket.close(code=1008)
            return None
        return player

    def get_room_by_id(self, room_id):
        try:
            return next(x for x in self.rooms if x.id == int(room_id))
        except StopIteration:
            return None

    async def create_room(self):
        id = math.floor(random() * 1000)
        try:
            room = Room(id, 15, 10)
        except GameException:
            return

        self.rooms.append(room)
        await self.notify()
        return id

    async def controller(self, room_id, websocket: WebSocket):
        room = self.get_room_by_id(room_id)
        if not room:
            return

        player = self.get_current_player(websocket)
        if not player:
            return

        try:
            async for _ in room.listen(player, websocket):
                await self.notify()
        except WebSocketDisconnect:
            if len(room.sockets) == 0:
                self.rooms.remove(room)
            await self.notify()

    async def notify(self):
        for listener in self.listeners:
            await listener.update()
