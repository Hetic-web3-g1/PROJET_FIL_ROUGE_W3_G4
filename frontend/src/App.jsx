import React, { useEffect, useState } from 'react';
import './App.css';
import { Landing } from './pages/landing/Landing.jsx';
import {ModalCreateMasterclass} from './components/Modal/modalcreatemasterclass/ModalCreateMasterclass.jsx'

function App() {
  return (
    <>
      <ModalCreateMasterclass />
    </>
  );
}

export default App;