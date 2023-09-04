import React, {useState, useContext} from 'react'
import { ReactReduxContext } from 'react-redux'

import './DashboardProfessor.css'

import Field from '../../field/Field'
// import Uploadcard from '../../upload/UploadCard'
import CardInstrument from '../../cardInstrument/CardInstrument'

import Instruments from '../../../constants/instruments'

export const DashboardProfessor = ({masterclassData, handleSave, professorData, type}) => {

    const { store } = useContext(ReactReduxContext)

    const [instrument, setInstrument] = React.useState(professorData?.instrument);
    const [firstName, setFirstName] = React.useState(professorData?.first_name);
    const [lastName, setLastName] = React.useState(professorData?.last_name);
    const [bio, setBio] = React.useState(professorData?.content);
    const [nationality, setNationality] = React.useState(professorData?.nationality);
    const [website, setWebsite] = React.useState(professorData?.website);
    const [awards, setAwards] = React.useState(professorData?.award);
    const [tmpAward, setTmpAward] = React.useState('');

    const [searchProfessorData, setSearchProfessorData] = useState([])
    const [masterclass, setMasterclass] = useState([])
    const [tmpProf, setTmpProf] = useState('')

    const setProfessor = (professor) => {
        var newMasterclassData = masterclassData
        setTmpProf(professor.first_name + ' ' + professor.last_name)
        setSearchProfessorData([])
        if (type == 'professor') {
            newMasterclassData.teacher_bio_id = professor?.id
        } else {
            newMasterclassData.composer_bio_id = professor?.id
        }
        newMasterclassData.updated_by = store?.getState().user.user_id
        newMasterclassData.updated_at = new Date()
        setMasterclass(newMasterclassData)
    }

    const handleSearch = (e) => {
        setTmpProf(e.target.value)
        const Options = {
            method: 'GET',
            headers:  { 'Content-Type': 'application/json', 'accept': 'application/json', 'authorization': `${store.getState().user.user_token}`},
          };
          fetch(`http://${import.meta.env.VITE_API_ENDPOINT}/tags/search/${e.target.value}?tables=biography`, Options).then((response) => response.json()).then(data => {
            setSearchProfessorData(data)
          });
    }

    const handleInstrument = (instrument) => {
        setInstrument([instrument]);
    };

    return (
        <div className='professor'>
            {!professorData?.id ? (
            <>
                <div className='professor-search'>
                    <div className="professor-searchbar">
                        <Field placeholder={`Search for a ${type}`} value={tmpProf} onChangeCallback={handleSearch}/>
                    </div>
                    <ul className="professor-list">
                        {searchProfessorData[0]?.map((professor) => {
                            return (
                                <li className="li-custom font professor-list-content" onClick={() => (setProfessor(professor))}>
                                    {professor.first_name} {professor.last_name}
                                </li>
                            )
                        })}
                    </ul>
                    <button onClick={e => {e.preventDefault; handleSave(masterclass)}}>Save</button>
                </div>
                <hr/>
            </>
            ) :  null }
            <div className="dashboard-prof-content">
                <div className="dashboard-prof-infos">
                    <div className="dashboard-prof-infos-1">
                        <div className="dashboard-prof-infos-field marg-right">
                            First Name
                            <Field placeholder="First Name"  value={firstName} onChangeCallback={(e) => setFirstName(e.target.value)}/>
                        </div>
                        <div className="dashboard-prof-infos-field marg-right">
                            Last Name
                            <Field placeholder="Last Name" value={lastName} onChangeCallback={(e) => setLastName(e.target.value)}/>
                        </div>
                        {/* <div className="dashboard-prof-background-wrapper">
                            <span>Avatar</span>
                                <div className="dashboard-prof-background-upload">
                                    <Uploadcard/>
                                </div>
                        </div> */}
                    </div>
                </div>
                <div className="dashboard-prof-instrument-wrapper">
                    Instruments
                    <div className="dashboard-prof-instrument">
                        {Instruments?.map((instrument, index) => {
                            return (
                                <div className="instrument-card">
                                    <CardInstrument key={`modal-instrument-card-${index}`} name={instrument} legend={true} onClick={handleInstrument}/>
                                </div>
                            )
                        })}
                    </div>
                </div>       
                <div>
                    <div className='field-container'>
                        <div className='dashboard-prof-infos-field marg-right'>
                            <span>Nationality</span>
                            <Field placeholder="Nationality"  value={nationality} onChange={(e) => setNationality(e.target.value)}/>
                        </div>
                        <div className='dashboard-prof-infos-field marg-width'>
                            <span>Website</span>
                            <Field placeholder="Website" value={website} onChange={(e) => setWebsite(e.target.value)}/>
                        </div>
                    </div>
                    <div className='dashboard-prof-infos-field full-width'>
                        <span>Awards</span>
                        {
                            awards?.map((award, index) => {
                                return(
                                    <div className='dashboard-prof-award-field'>
                                        <Field placeholder="Award" value={award} onChange={(e) => 
                                            {
                                            let Array = [...awards];
                                            Array[index] = e.target.value;
                                            setAwards(Array);
                                            }
                                        }/>
                                    </div>
                                )
                            })
                        }
                        <div className='dashboard-prof-infos-field-add'>
                            <img src={'../../src/assets/plus.svg'} alt="plus" style={{marginRight: '1vw', cursor: 'pointer'}} onClick={() => setAwards([...awards, tmpAward])}/>
                            <Field placeholder="Awards" onChange={(e) => setTmpAward([e.target.value])}/>
                        </div>
                    </div>
                </div> 
                <div style={{ display: 'flex','flex-direction': 'column'}}>
                    <span>Biography</span>
                    <textarea className="dashboard-prof-textarea"  value={bio} placeholder="..." row='20' onChange={(e) => setBio(e.target.value)}/>
                </div>
            </div>
        </div>
    );
};

export default DashboardProfessor;