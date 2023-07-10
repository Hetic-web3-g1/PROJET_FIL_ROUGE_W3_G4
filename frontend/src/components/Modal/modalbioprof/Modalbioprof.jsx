import React from 'react'
import propTypes from 'prop-types'


import Modal from '../Modal'
import CardInstrument from '../../cardInstrument/CardInstrument'

import './modalbioprof.css'
import Instruments from '../../../constants/instruments'
import Field from '../../field/Field'
import Uploadcard from '../../upload/UploadCard'


export const ModalBioProf = ({ handleClose, store }) => {

    const [status, setStatus] = React.useState(1);

    const radioHandler = (status) => {
        setStatus(status);
      };

    const [instrument, setInstrument] = React.useState([]);
    const [firstName, setFirstName] = React.useState('');
    const [lastName, setLastName] = React.useState('');
    const [bio, setBio] = React.useState('');
    const [nationality, setNationality] = React.useState('');
    const [website, setWebsite] = React.useState('');
    const [awards, setAwards] = React.useState([]);
    const [type, setType] = React.useState('Professor');
    const [body, setBody] = React.useState();

    const createdBy = store.getState().user.profile.id;

    const handleInstrument = (instrument) => {
        setInstrument([instrument]);
    };

    const handleSave = () => {
        if (status === 1) {
            setBody({
                instrument: instrument,
                first_name: firstName,
                last_name: lastName,
                bio: bio,
                nationality: nationality,
                website: website,
                awards: awards,
                type: type,
                created_by: createdBy,
            });
        } else {
            setBody({
                instrument: instrument,
                first_name: firstName,
                last_name: lastName,
                bio: bio,
                type: type,
                created_by: createdBy,
            });
        }
        const bioOptions = {
          method: 'POST',
          headers: { 'Content-Type': 'application/json', 'accept': 'application/json', 'authorization': `${store.getState().user.user_token}` },
          body: JSON.stringify(body),
        };
        fetch('http://localhost:4000/biographies/biography', bioOptions).then((response) => response.json()).then(data => {
          if (data.detail[0].msg != "field required") {
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
                        <Field placeholder="First Name" onChange={(e) => setFirstName(e.target.value)}/>
                    </div>
                    <div className="modal-bio-prof-infos-field marg-right">
                        Last Name
                        <Field placeholder="Last Name" onChange={(e) => setLastName(e.target.value)}/>
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

            </div>
            <div className="modal-bio-prof-instrument-wrapper">
                Instruments
                <div className="modal-bio-prof-instrument">
                    {Instruments.map((instrument, index) => {
                        return (
                            <div className="instrument-card">
                                <CardInstrument key={`modal-instrument-card-${index}`} name={instrument} legend={true} onClick={handleInstrument}/>
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
                            <Field placeholder="Nationality" onChange={(e) => setNationality(e.target.value)}/>
                        </div>
                        <div className='modal-bio-prof-infos-field fix-width'>
                            <span>Website</span>
                            <Field placeholder="Website" onChange={(e) => setWebsite(e.target.value)}/>
                        </div>
                    </div>
                    <div className='modal-bio-prof-infos-field full-width'>
                        <span>Awards</span>
                        <Field placeholder="Awards" onChange={(e) => setAwards([e.target.value])}/>
                    </div>
                </div> 
            : null }
   
            <div style={{ display: 'flex','flex-direction': 'column'}}>
                <span>Biography</span>
                <textarea className="modal-bio-prof-textarea" placeholder="..." row='20' onChange={(e) => setBio(e.target.value)}/>
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
