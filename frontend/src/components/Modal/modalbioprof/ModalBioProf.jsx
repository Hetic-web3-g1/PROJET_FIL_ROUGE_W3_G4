import React, { useEffect } from 'react'
import propTypes from 'prop-types'

import Modal from '../Modal'
import CardInstrument from '../../cardInstrument/CardInstrument'

import './ModalBioProf.css'
import Instruments from '../../../constants/instruments'
import Field from '../../field/Field'
import Uploadcard from '../../upload/UploadCard'


export const ModalBioProf = ({ handleClose, store, DefaultValue }) => {

    const [status, setStatus] = React.useState(1);
    const [instrument, setInstrument] = React.useState(DefaultValue.instrument || []);
    const [firstName, setFirstName] = React.useState(DefaultValue.first_name || '');
    const [lastName, setLastName] = React.useState(DefaultValue.last_name  || '');
    const [bio, setBio] = React.useState(DefaultValue.content  || '');
    const [nationality, setNationality] = React.useState(DefaultValue.nationality  || '');
    const [website, setWebsite] = React.useState(DefaultValue.website  || '');
    const [awards, setAwards] = React.useState(DefaultValue.award || []);
    const [tmpAward, setTmpAward] = React.useState('');
    const [type, setType] = React.useState('Professor');

    const createdBy = store.getState().user.profile.id;
    
    const radioHandler = (status) => {
        setStatus(status);
    };

    const handleInstrument = (instrument) => {
        setInstrument([instrument]);
    };

    const handleSave = () => {
        const bioOptions = {
          method: 'POST',
          headers: { 'Content-Type': 'application/json', 'accept': 'application/json', 'authorization': `${store.getState().user.user_token}` },
          body : JSON.stringify({
                instrument: instrument,
                first_name: firstName,
                last_name: lastName,
                content: bio,
                nationality: nationality,
                website: website,
                award: awards,
                type: type,
                created_by: createdBy,
            }),
        };
        fetch(`http://${import.meta.env.VITE_API_ENDPOINT}/biographies/biography`, bioOptions).then((response) => response.json()).then(data => {
          if (data?.detail[0].msg != "field required") {
            handleClose();
          } else {
            alert('Invalid data');
          }
        });
    };

    const bioContent = (
        <div className="modal-bio-prof-content">
            <div className="modal-bio-prof-infos">
                <div className="modal-bio-prof-infos-1">
                    <div className="modal-bio-prof-infos-field marg-right">
                        First Name
                        <Field placeholder="First Name" value={firstName} onChange={(e) => setFirstName(e.target.value)}/>
                    </div>
                    <div className="modal-bio-prof-infos-field marg-right">
                        Last Name
                        <Field placeholder="Last Name" value={lastName} onChange={(e) => setLastName(e.target.value)}/>
                    </div>
                    <div className="modal-bio-prof-infos-checkbox">
                        <div className="modal-bio-prof-infos-element">
                            <input checked={status === 1} onClick={(e) => {radioHandler(1); setType('Professor')}}  type='radio' id='radio-1' placeholder="Professor" name='user' unchecked/>
                            <span>Professor</span>

                        </div>
                        <div className="modal-bio-prof-infos-element">
                            <input checked={status === 2} onClick={(e) => {radioHandler(2); setType('Compositor')}} type='radio' id='radio-2' placeholder="Compositor" name='user' unchecked/>
                            <span>Compositor</span>

                        </div>
                    </div>
                        <div className="modal-bio-prof-background-wrapper">
                        <span>Avatar</span>
                            <div className="modal-bio-prof-background-upload">
                                <Uploadcard/>
                            </div>
                        </div>
                </div>
            <div>
                <img></img>
            </div>
            </div>
            <div className="modal-bio-prof-instrument-wrapper">
                Instruments
                <div className="modal-bio-prof-instrument">
                    {Instruments.map((instrumen, index) => {
                        return (
                            <div className="instrument-card">
                                <CardInstrument Defaultvalue={instrument[0]} key={`modal-instrument-card-${index}`} name={instrumen} legend={true} onClick={handleInstrument}/>
                            </div>
                        )
                    })}
                </div>
            </div>

            { status === 1 ?        
                <div>
                    <div className='field-container'>
                        <div className='modal-bio-prof-infos-field marg-right'>
                            <span>Nationality</span>
                            <Field placeholder="Nationality" value={nationality} onChange={(e) => setNationality(e.target.value)}/>
                        </div>
                        <div className='modal-bio-prof-infos-field fix-width'>
                            <span>Website</span>
                            <Field placeholder="Website" value={website} onChange={(e) => setWebsite(e.target.value)}/>
                        </div>
                    </div>
                    <div className='modal-bio-prof-infos-field full-width'>
                        <span>Awards</span>
                        {
                            awards.map((award, index) => {
                                return(
                                    <div className='modal-bio-prof-award-field'>
                                        <Field placeholder="Award" value={award} onChange={e =>
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
                        <div className='modal-bio-prof-infos-field-add'>
                            <img src={'../../src/assets/plus.svg'} alt="plus" style={{marginRight: '1vw', cursor: 'pointer'}} onClick={() => setAwards([...awards, tmpAward])}/>
                            <Field placeholder="Awards" onChange={(e) => setTmpAward([e.target.value])}/>
                        </div>
                    </div>
                </div> 
            : null }
   
            <div style={{ display: 'flex','flex-direction': 'column'}}>
                <span>Biography</span>
                <textarea value={bio} className="modal-bio-prof-textarea" placeholder="..." row='20' onChange={(e) => setBio(e.target.value)}/>
            </div>
        </div>
    );

    return(
        <Modal title="Biography" content={bioContent} size='full' handleClose={handleClose} handleSave={handleSave} />
    );
};

ModalBioProf.propTypes = {
    biography: propTypes.string,
    content: propTypes.string,
    handleClose: propTypes.func,
};

export default ModalBioProf;
