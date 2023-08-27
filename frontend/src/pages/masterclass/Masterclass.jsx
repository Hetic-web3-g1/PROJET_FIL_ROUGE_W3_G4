import React, {useEffect, useState, useContext} from "react";
import { ReactReduxContext } from 'react-redux'

import './Masterclass.css'

import { Header } from "../../components/header/Header";
import { Tabs } from "../../components/tabs/Tabs";
import { UploadCard } from "../../components/upload/UploadCard";

import DashboardVideo from "../../components/dashboard/video/DashboardVideo";
//import DashboardPartition from "../../components/dashboard/DashboardPartition";
//import DashboardWorkAnalysis from "../../components/dashboard/DashboardWorkAnalysis";
import DashboardProfessor from "../../components/dashboard/professor/DashboardProfessor";
import DashboardTeam from "../../components/dashboard/team/DashboardTeam";

import MasterClassData from '../../mocks/masterClassMocks'

export const Masterclass = () => {

  const { store } = useContext(ReactReduxContext)

  const [component, setComponent] = useState('');
  const [tabName, setTabName] = useState('');
  const [masterclassData, setMasterclassData] = useState();
  const [composerData, setComposerData] = useState();
  const [professorData, setProfessorData] = useState();
  const masterclassId = window.location.href.split('/')[4];
  
  useEffect(() => {
    const Options = {
      method: 'GET',
      headers:  { 'Content-Type': 'application/json', 'accept': 'application/json', 'authorization': `${store.getState().user.user_token}`},
    };
    fetch(`http://localhost:4000/masterclasses/masterclass/${masterclassId}`, Options).then((response) => response.json()).then(data => {
      setMasterclassData(data)
    });
  },[]);

  useEffect(() => {
    if (masterclassData) {
      const Options = {
        method: 'GET',
        headers:  { 'Content-Type': 'application/json', 'accept': 'application/json', 'authorization': `${store.getState().user.user_token}`},
      };
      fetch(`http://localhost:4000/biographies/biography/${masterclassData.teacher_bio_id}`, Options).then((response) => response.json()).then(data => {
        setProfessorData(data)
      });
    }
  },[masterclassData]);

  useEffect(() => {
    if (masterclassData) {
      const Options = {
        method: 'GET',
        headers:  { 'Content-Type': 'application/json', 'accept': 'application/json', 'authorization': `${store.getState().user.user_token}`},
      };
      fetch(`http://localhost:4000/biographies/biography/${masterclassData.composer_bio_id}`, Options).then((response) => response.json()).then(data => {
        setComposerData(data)
      });
    }
  },[masterclassData]);

  console.log(masterclassData)

  const handleSave = (e, newMasterclassData) => {
    e.preventDefault();
    const userOptions = {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json', 'accept': 'application/json', 'authorization': `${store.getState().user.user_token}` },
        body: JSON.stringify({
          academy_id: newMasterclassData.academy_id,
          composer_bio_id: newMasterclassData.composer_bio_id,
          created_at: newMasterclassData.created_at,
          description: newMasterclassData.description,
          id: newMasterclassData.id,
          instrument: newMasterclassData.instrument,
          partition_id: newMasterclassData.partition_id,
          status: newMasterclassData.status,
          teacher_bio_id: newMasterclassData.teacher_bio_id,
          title: newMasterclassData.title,
          updated_at: newMasterclassData.updated_at,
          updated_by: newMasterclassData.updated_by,
          work_analysis_id: newMasterclassData.work_analysis_id,
        }),
    }
    fetch(`http://${import.meta.env.VITE_API_ENDPOINT}/masterclasses/masterclass/${masterclassData.id}`, userOptions).then((response) => response.json()).then(data => {
        console.log(data);
    });
  }

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
        setComponent(<DashboardTeam/>);
        break;

      case 'Video':
      setComponent(<DashboardVideo/>);
      break;

      case 'Partition':
        setComponent(<></>);
        break;
      
      case 'Work analysis':
        setComponent(<></>);
        break;

      case 'Professor':
        setComponent(<DashboardProfessor masterclassData={masterclassData} handleSave={handleSave} professorData={professorData} type={"professor"} key={"professor"}/>);
        break;

      case 'Compositor':
        setComponent(<DashboardProfessor masterclassData={masterclassData} handleSave={handleSave} professorData={composerData} type={"composer"} key={"composer"}/>);
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

      <div  className="masterclass-page-container">

        <div className="masterclass-overview" >
          
          <h1 >{masterclassData?.title}</h1>
          <div style={tabName !== 'Masterclass' ? {display: 'none'} : null}>
            
          
          <div className="masterclass-information" >

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
                <span>{masterclassData?.instrument[0]}</span>
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

            <div className="masterclass-information-col" >
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
        </div>
        <div className="masterclass-status" style={tabName !== 'Masterclass' ? {display: 'none'} : null} >
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