import React, { useEffect, useState } from 'react';
import YouTube from 'react-youtube';
import './App.css';
import kirbok from './assets/kirbok.jpg';

function App() {
  const [message, setMessage] = useState('');

  useEffect(() => {
    fetch('http://localhost:4000/')
      .then((response) => response.json())
      .then((data) => {
        setMessage(data.msg); // Set the message state
      });
  }, []);

  const videoId = 'LurJCpb4rRE'; // YouTube video ID

  return (
    <>
      <div>
        <YouTube videoId={videoId} />
      </div>
      <h1>Projet de fou de fin de l'année</h1>
      <div>
        <h3>Message from backend</h3>
        <h3>{message}</h3>
      </div>
    </>
  );
}

export default App;