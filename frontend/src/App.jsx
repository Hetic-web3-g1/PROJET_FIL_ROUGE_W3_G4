import React, { useEffect, useState } from 'react';
import './App.css';

import { useSelector, useDispatch } from 'react-redux'
import { decrement, increment } from './features/reduxExample'
import { Login } from './pages/login/Login.jsx';

function App() {
  const count = useSelector((state) => state.counter.value)
  const dispatch = useDispatch()

  return (
    
    <>
    <Login />
      {/* <h1>Projet de fou de fin de l'année</h1>
      <div>
        <button
            aria-label="Increment value"
            onClick={() => dispatch(increment())}
          >
            Increment
          </button>
          <span>{count}</span>
          <button
            aria-label="Decrement value"
            onClick={() => dispatch(decrement())}
          >
            Decrement
          </button>
        </div> */}
    </>
  );
}

export default App;