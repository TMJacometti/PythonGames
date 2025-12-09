# server.py
import json
from typing import Dict, List

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from game import CheckersGame, InvalidMove

app = FastAPI()

# CORS liberado (ambiente dev)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Servir arquivos estáticos (HTML/JS)
app.mount("/static", StaticFiles(directory="static"), name="static")


class Room:
    def __init__(self):
        self.game = CheckersGame()
        self.clients: Dict[str, WebSocket] = {}  # "red" / "black"

    def is_full(self) -> bool:
        return len(self.clients) >= 2

    def get_player_color(self) -> str:
        if "red" not in self.clients:
            return "red"
        elif "black" not in self.clients:
            return "black"
        else:
            raise Exception("Sala cheia")

    def get_opponent_color(self, color: str) -> str:
        return "black" if color == "red" else "red"

    def get_clients(self) -> List[WebSocket]:
        return list(self.clients.values())


rooms: Dict[str, Room] = {}


@app.get("/")
async def root():
    return {"message": "Servidor de Dama Multiplayer. Abra /static/index.html no navegador."}


@app.websocket("/ws/{room_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: str):
    await websocket.accept()

    if room_id not in rooms:
        rooms[room_id] = Room()
    room = rooms[room_id]

    if room.is_full():
        await websocket.send_text(json.dumps({"type": "error", "message": "Sala cheia."}))
        await websocket.close()
        return

    # Registra jogador
    color = room.get_player_color()
    room.clients[color] = websocket

    await websocket.send_text(json.dumps({
        "type": "joined",
        "you": color,
    }))

    # Se os dois jogadores conectaram, manda estado inicial pra ambos
    if len(room.clients) == 2:
        await broadcast_state(room)

    try:
        while True:
            data = await websocket.receive_text()
            msg = json.loads(data)

            if msg.get("type") == "move":
                from_pos = msg.get("from")  # [r, c]
                to_pos = msg.get("to")      # [r, c]

                try:
                    room.game.move(color, tuple(from_pos), tuple(to_pos))
                except InvalidMove as e:
                    await websocket.send_text(json.dumps({
                        "type": "error",
                        "message": str(e),
                    }))
                    continue

                await broadcast_state(room)
    except WebSocketDisconnect:
        # Remove jogador e reseta sala se necessário
        if color in room.clients:
            del room.clients[color]
        if len(room.clients) == 0:
            # reseta a sala totalmente
            del rooms[room_id]


async def broadcast_state(room: Room):
    state = room.game.serialize()
    for color, ws in room.clients.items():
        await ws.send_text(json.dumps({
            "type": "state",
            "you": color,
            **state,
        }))
