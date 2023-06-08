import React, { useEffect, useState } from 'react';
import './App.css';
import { Landing } from './pages/landing/Landing.jsx';
import {ModalBio} from './components/Modal/modalbio/Modalbio.jsx';

function App() {
  return (
    <>
      <ModalBio />
    </>
  );
}

export default App;