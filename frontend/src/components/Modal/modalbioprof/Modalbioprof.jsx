import React from 'react'
import propTypes from 'prop-types'


import Modal from '../Modal'
import CardInstrument from '../../cardInstrument/CardInstrument'

import './modalbioprof.css'
import Instruments from '../../../constants/instruments'
import Field from '../../field/Field'
import Uploadcard from '../../upload/UploadCard'
import Professorfields from '../../professorfields/Professorfields'


export const ModalBioProf = ({ biography, content, handleClose, handleSave, isChecked }) => {

    const [status, setStatus] = React.useState(isChecked = 1);

    const radioHandler = (status) => {
        setStatus(status);
      };

    const [instrument, setInstrument] = React.useState('');

    const handleInstrument = (instrument) => {
        setInstrument(instrument);
    };



    const bioContent = (
        <div className="modal-bio-prof-content">
            <div className="modal-bio-prof-infos">
                <div className="modal-bio-prof-infos-1">
                    <div className="modal-bio-prof-infos-field marg-right">
                        First Name
                        <Field placeholder="First Name"/>
                    </div>
                    <div className="modal-bio-prof-infos-field marg-right">
                        Last Name
                        <Field placeholder="Last Name"/>
                    </div>
                    <div className="modal-bio-prof-infos-checkbox">
                        <div className="modal-bio-prof-infos-element">
                            <input checked={status === 1} onClick={(e) => radioHandler(1)}  type='radio' id='radio-1' placeholder="Professor" name='user' unchecked/>
                            <span>Professor</span>

                        </div>
                        <div className="modal-bio-prof-infos-element">
                            <input checked={status === 2} onClick={(e) => radioHandler(2)} type='radio' id='radio-2' placeholder="Compositor" name='user' unchecked/>
                            <span>Compositor</span>

                        </div>
                    </div>
                    {/* <div className='upload-avatar'>
                        <input type="file" id="avatar" name="avatar" accept="image/png, image/jpeg"/>
                    </div> */}
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

            { status === 1 ? < Professorfields/> : null }
            { status === 2 ? null : null }
   
            <div style={{ display: 'flex','flex-direction': 'column'}}>
                <span>Biography</span>
                <textarea className="modal-bio-prof-textarea" placeholder="..." row='20'/>
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
