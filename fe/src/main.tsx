import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { Rooms } from './Rooms.tsx'
import "./style.css"

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <Rooms />
  </StrictMode>,
)
