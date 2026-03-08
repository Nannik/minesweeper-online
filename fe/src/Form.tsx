import type { Room } from "./Rooms"

interface FormProps {
  rooms: Room[]
  player: string
  onPlayerChange: (player: string) => void
  createRoom: () => void
  setCurrentRoom: (room: number | null) => void
}

export const Form = (props: FormProps) => {
  const {
    rooms,
    player,
    onPlayerChange,
    createRoom,
    setCurrentRoom
  } = props;

  return (
    <div className="form">
      <input
        value={player}
        type='text' 
        onChange={(e) => onPlayerChange(e.target.value)}
      />

      <button
        disabled={player == ''}
        onClick={createRoom}
      >
        Create room
      </button >
      {rooms.map(room => (
        <button
          key={room.id}
          disabled={player == ''}
          onClick={() => setCurrentRoom(room.id)}
        >
          <b>Connect</b> to {room.id}: Players: {room.players_count}
        </button>
      ))}
    </div>

  )
}
