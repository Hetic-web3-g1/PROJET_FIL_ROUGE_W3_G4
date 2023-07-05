import React, { useEffect, useState } from 'react';
import './App.css';
import { Landing } from './pages/landing/Landing.jsx';
import {ModalBioProf} from './components/Modal/modalbioprof/Modalbioprof.jsx';
import ModalBio from './components/Modal/modalbio/Modalbio';

function App() {
  return (
    <>
      <ModalBioProf />
    </>
  );
}

export default App;