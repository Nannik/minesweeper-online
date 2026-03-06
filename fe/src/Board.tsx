import { useEffect, useRef, useState } from "react";

interface BoardProps {
  room: number
  player: string
  onClose: () => void
}

const mapCellValue = (v: number) => {
  if (v > 0) return v
  return ''
}

export const Board = (props: BoardProps) => {
  const {
    room,
    player,
    onClose
  } = props;

  const ref = useRef(null)
  const [ws, setWs] = useState<WebSocket | null>(null)
  const [board, setBoard] = useState<[][]>([])
  const [isGameOver, setIsGameOver] = useState(false)

  useEffect(() => {
    setBoard([])
  }, [room, player])

  useEffect(() => {
    console.log(import.meta.env.VITE_API_HOST + ':' + import.meta.env.VITE_API_PORT)
    let ws = new WebSocket(`/ws/${room}?player=${player}`);

    ws.onmessage = (e) => {
      let data = JSON.parse(e.data);
      if (data.type && data.type == "GameOver") {
        setIsGameOver(true)
      }

      if (data && data.board) {
        setBoard(data.board);
      }
    }

    ws.onopen = (e) => {
      setWs(ws)
    }

    ws.onclose = (e) => {
      setWs(null)
      onClose()
    }
  }, [room, player])

  const handleClose = () => {
    ws.close()
    onClose()
  }

  const send = (e, x, y) => {
    let type = 'REVEAL'
    if (e.button == 2) {
      type = 'FLAG'
    }
    if (!isGameOver) {
      ws.send(JSON.stringify({ type, x, y }))
    }
  }

  let cellSize = 0;
  if (ref.current && board.length > 0) {
    let cellWidth = (ref.current.offsetWidth) / board[0].length - 2
    let cellHeight = (window.innerHeight * 2.8) / board.length
    cellSize = Math.min(cellHeight, cellWidth)
  }

  return (
    <div>
      Playing on {room}
      <button onClick={handleClose}>Disconnect</button>

      {isGameOver && (
        <div>
          Game Over
        </div>
      )}
      <div
        ref={ref}
        className="grid"
        onContextMenu={(e) => e.preventDefault()}
      >
        {board.map((row, y) => (
          <div className="row">
            {row.map((cell, x) => (
              <div 
                style={{
                  width: cellSize + 'px',
                  height: cellSize + 'px',
                  lineHeight: cellSize + 'px'
                }}
                className={`
                  cell 
                  ${cell >= 0 && 'revealed'}
                  ${cell == -1 && 'mine'}
                  ${cell == -3 && 'flag'}
                `}
                onMouseDown={(e) => send(e, x, y)}
              >
                {mapCellValue(cell)}
              </div>
            ))}
          </div>
        ))}
      </div>
    </div>
  )
}
