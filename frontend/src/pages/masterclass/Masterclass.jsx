import React, {useEffect, useState, useContext} from "react";
import { ReactReduxContext } from 'react-redux'

import './Masterclass.css'

import { Header } from "../../components/header/Header";
import { Tabs } from "../../components/tabs/Tabs";
import { UploadCard } from "../../components/upload/UploadCard";

import MasterClassData from '../../mocks/masterClassMocks'

export const Masterclass = () => {

  const { store } = useContext(ReactReduxContext)

  const [component, setComponent] = useState('');
  const [tabName, setTabName] = useState('');
  const [masterclassData, setMasterclassData] = useState();
  const masterclassId = window.location.href.split('/')[4];
  
  useEffect(() => {
    const Options = {
      method: 'GET',
      headers:  { 'Content-Type': 'application/json', 'accept': 'application/json', 'authorization': `${store.getState().user.user_token}`},
    };
    fetch(`http://localhost:4000/masterclasses/${masterclassId}`, Options).then((response) => response.json()).then(data => {
      setMasterclassData(data)
    });
  },[])

  /**
   * Get data from tabs component and depending of the value set the corresponding component in the HTML.
   * @param childData Data from tabs component
   */
  function handleCallback(childData) {
    setTabName(childData);
    switch (childData) {
      case 'Masterclass':
        setComponent(<UploadCard/>)
        break;

      case 'Team':
        setComponent(<></>);
        break;

      case 'Video':
      setComponent(<></>);
      break;

      case 'Partition':
        setComponent(<></>);
        break;
      
      case 'Work analysis':
        setComponent(<></>);
        break;

      case 'Professor':
        setComponent(<></>);
        break;

      case 'Compositor':
        setComponent(<></>);
        break;

      default:
        break;
    }
}
  useEffect(() => {
    handleCallback('Masterclass');
  }, []);

  return (
    <div className="masterclass-page">
      <Header/>

      <div style={tabName !== 'Masterclass' ? {display: 'none'} : null} className="masterclass-page-container">

        <div className="masterclass-overview">
          <h1>{MasterClassData.title}</h1>

          <div className="masterclass-information">

            <div className="masterclass-information-col">
              <section>
                <span className="masterclass-span">Composer</span>
                <span>{MasterClassData.composer}</span>
              </section>
              <section className="masterclass-section">
                <span className="masterclass-span">Professor</span>
                <span>{MasterClassData.professor}</span>
              </section>
              <section className="masterclass-section">
                <span className="masterclass-span">Instruments</span>
                <span>{MasterClassData.instruments}</span>
              </section>
              <section className="masterclass-section">
                <span className="masterclass-span">Producer</span>
                <span>{MasterClassData.producer}</span>
              </section>
              <section className="masterclass-section">
                <span className="masterclass-span">Spoken Language</span>
                <span>{MasterClassData.spoken_language}</span>
              </section>
            </div>

            <div className="masterclass-information-col">
              <section>
                <span className="masterclass-span">Piece</span>
                <span>{MasterClassData.piece}</span>
              </section>
              <section className="masterclass-section">
                <span className="masterclass-span">Student</span>
                <span>{MasterClassData.student}</span>
              </section>
              <section className="masterclass-section">
                <span className="masterclass-span">Date</span>
                <span>{MasterClassData.date}</span>
              </section>
              <section className="masterclass-section">
                <span className="masterclass-span">Duration</span>
                <span>{MasterClassData.duration}</span>
              </section>
              <section className="masterclass-section">
                <span className="masterclass-span">Subtitle Languages</span>
                <span>{MasterClassData.subtitle_languages}</span>
              </section>
            </div>
          </div>
        </div>
        <div className="masterclass-status">
          <h2>Status</h2>
          <section className="masterclass-section-status">
            <span>Team</span>
            <img src="..\src\assets\status\done.svg" alt="done" />
          </section>
          <section className="masterclass-section-status">
            <span>Video</span>
            <img src="..\src\assets\status\incomplete.svg" alt="incomplete" />
          </section>
          <section className="masterclass-section-status">
            <span>Partition</span>
            <img src="..\src\assets\status\incomplete.svg" alt="incomplete" />
          </section>
          <section className="masterclass-section-status">
            <span>Biographie P.</span>
            <img src="..\src\assets\status\done.svg" alt="done" />
          </section>
          <section className="masterclass-section-status">
            <span>Biographie C.</span>
            <img src="..\src\assets\status\incomplete.svg" alt="incomplete" />
          </section>
          <section className="masterclass-section-status">
            <span>Work Analysis</span>
            <img src="..\src\assets\status\done.svg" alt="done" />
          </section>
        </div>

      </div>

      <Tabs callback={handleCallback}/>

      <div className="masterclass-component-render">
        {component}
      </div>

    </div>
    );
}

export default Masterclass;