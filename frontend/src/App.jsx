import { useState } from 'react'
import kirbok from './assets/kirbok.jpg'
import './App.css'

function App() {
  const [count, setCount] = useState(0)

  return (
    <>
      <div>
        <a href="https://youtu.be/LurJCpb4rRE" target="_blank">
          <img src={kirbok} className="logo react" alt="kirbok" />
        </a>
      </div>
      <h1>Projet de fou de fin de l'année ouais</h1>
      <div className="card">
        <button onClick={() => setCount((count) => count + 1)}>
          count is {count}
        </button>
      </div>
    </>
  )
}

export default App
