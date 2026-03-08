from fastapi import WebSocket, WebSocketDisconnect
from app.Board import Board
from json import JSONDecodeError


class Socket:
    player: str
    socket: WebSocket

    def __init__(self, player: str, socket: WebSocket):
        self.player = player
        self.socket = socket


class Room:
    id: int
    size: int
    mines_count: int
    sockets: list[Socket] = []
    board: Board

    def __init__(self, id, size, mines_count):
        self.id = id
        self.size = size
        self.mines_count = mines_count
        self.board = Board(size, size, mines_count)

    async def send(self):
        print(self.sockets)
        for socket in self.sockets:
            await socket.socket.send_json({
                "type": "GameOver" if self.board.is_game_over else "Update",
                "board": self.board.get()
            })

    async def listen(self, player: str, websocket: WebSocket):
        await websocket.accept()
        current_socket = Socket(player, websocket)
        self.sockets.append(current_socket)
        yield

        await self.send()
        try:
            while True:
                try:
                    json = await websocket.receive_json()
                except JSONDecodeError:
                    continue

                if 'type' not in json:
                    continue

                if json['type'] == 'RESTART':
                    self.board = Board(
                    self.size,
                    self.size,
                    self.mines_count
                )

                if (
                    ('x' in json) and
                    ('y' in json) and
                    isinstance(json['x'], int) and
                    isinstance(json['y'], int)
                ):
                    if json['type'] == 'FLAG':
                        self.board.flag(json['x'], json['y'])
                    else:
                        self.board.reveal(json['x'], json['y'])

                await self.send()

        except WebSocketDisconnect as e:
            self.sockets.remove(current_socket)
            raise e
