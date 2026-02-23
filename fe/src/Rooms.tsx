import { useState, useEffect } from "react"
import { api } from "./api"
import { Board } from "./Board"

type Room = {
  id: number,
  players_count: number
}

export const Rooms = () => {
  const [rooms, setRooms] = useState<Room[]>([])
  const [currentRoom, setCurrentRoom] = useState<number | null>(null)
  const [player, setPlayer] = useState('')

  useEffect(() => {
    let ws = new WebSocket(`http://localhost:8000/ws`);

    ws.onmessage = (e) => {
      setRooms(JSON.parse(e.data))
    }
  }, [])

  const createRoom = async () => {
    const res = await api.get<number>('/create_room')
    setCurrentRoom(res.data)
  }

  return (
    <div>
      {currentRoom ? (
        <Board 
          room={currentRoom}
          player={player}
          onClose={() => setCurrentRoom(null)}
        />
      ) : null}

      <input 
        disabled={currentRoom != null}
        type='text' onChange={(e) => setPlayer(e.target.value)} 
      />

      <button
        disabled={player == ''}
        onClick={createRoom}
      >
        Create room
      </button>
      <ul>
        {rooms.map(room => (
          <li>
            <span>{room.id}: Players: {room.players_count}</span>
            <button
              disabled={player == ''}
              onClick={() => setCurrentRoom(room.id)}
            >
              Connect
            </button>
          </li>
        ))}
      </ul>
    </div>
  )
}
