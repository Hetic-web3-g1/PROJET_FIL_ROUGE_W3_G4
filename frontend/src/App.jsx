import React, { useEffect, useState } from 'react';
import './App.css';
import { Landing } from './pages/landing/Landing.jsx';
import {ModalBioProf} from './components/Modal/modalbioprof/Modalbioprof.jsx';

function App() {
  return (
    <>
      <ModalBioProf />
    </>
  );
}

export default App;