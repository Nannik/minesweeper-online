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
  let wrapperWidth: number | string = '100%';
  if (ref.current && board.length > 0) {
    let cellWidth = (ref.current.offsetWidth) / board[0].length - 2
    let cellHeight = (window.innerHeight - 150) / board.length
    cellSize = Math.min(cellHeight, cellWidth)
    wrapperWidth = ((cellSize + 2) * board[0].length)
  }

  return (
    <div
      className="grid-wrapper"
      style={{
        width: wrapperWidth
      }}
    >
      <div
        ref={ref}
        className="grid"
        onContextMenu={(e) => e.preventDefault()}
      >
        {isGameOver && (
          <div
            className="board-overlay"
          >
            Game Over
            <div className="w-full">
              <button onClick={handleClose}>Try again</button>
            </div>
          </div>
        )}
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

      <div className="w-full">
        <button onClick={handleClose}>Disconnect</button>
      </div>
    </div>
  )
}
