import { useState, useEffect } from "react"
import { api } from "./api"
import { Board } from "./Board"
import { Form } from "./Form"

export type Room = {
  id: number,
  players_count: number
}

export const Rooms = () => {
  const [rooms, setRooms] = useState<Room[]>([])
  const [currentRoom, setCurrentRoom] = useState<number | null>(null)
  const [player, setPlayer] = useState(localStorage.getItem('player'))

  useEffect(() => {
    let ws = new WebSocket(`/ws`);

    ws.onmessage = (e) => {
      setRooms(JSON.parse(e.data))
    }
  }, [])

  const createRoom = async () => {
    try {
      const res = await api.get<number>('/create_room')
      setCurrentRoom(res.data)
    } catch (e) {
      alert(JSON.stringify(e))
    }
  }

  return (
    <div>
      {currentRoom ? (
        <Board 
          room={currentRoom}
          player={player}
          onClose={() => setCurrentRoom(null)}
        />
      ) : (
        <Form 
          rooms={rooms}
          player={player}
          onPlayerChange={(player) => {
            setPlayer(player)
            localStorage.setItem('player', player)
          }}
          createRoom={createRoom}
          setCurrentRoom={setCurrentRoom}
        />
      )}
    </div>
  )
}
