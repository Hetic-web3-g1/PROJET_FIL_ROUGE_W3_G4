import React, { useEffect, useState } from 'react';
import './App.css';
import { Landing } from './pages/landing/Landing.jsx';
import { ModalWorkanalysis } from './components/Modal/modalworkanalysis/ModalWorkanalysis.jsx';
import { ModalBioProf } from './components/Modal/modalbioprof/Modalbioprof.jsx';

function App() {
  return (
    <>
      <ModalWorkanalysis />
    </>
  );
}

export default App;