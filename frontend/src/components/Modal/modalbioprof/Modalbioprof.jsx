import React from 'react'
import propTypes from 'prop-types'

import Modal from '../Modal'
import CardInstrument from '../../cardInstrument/CardInstrument'

import './modalbioprof.css'
import Instruments from '../../../constants/instruments'
import Field from '../../field/Field'
import Uploadcard from '../../upload/UploadCard'

export const ModalBioProf = ({ biography, content, handleClose, handleSave }) => {

    const [instrument, setInstrument] = React.useState('');

    const handleInstrument = (instrument) => {
        setInstrument(instrument);
    };

    const bioContent = (
        <div className="modal-bio-prof-content">
            <div className="modal-bio-prof-infos">
                <div className="modal-bio-prof-infos-1">
                    <div className="modal-bio-prof-infos-field">
                        First Name
                        <Field placeholder="First Name"/>
                    </div>
                    <div className="modal-bio-prof-infos-field">
                        Last Name
                        <Field placeholder="Last Name"/>
                    </div>
                    <div className="modal-bio-prof-infos-checkbox">
                        <div className="modal-bio-prof-infos-element">
                            <Field type='checkbox' placeholder="Professor"/>
                            <span>Professor</span>

                        </div>
                        <div className="modal-bio-prof-infos-element">
                            <Field type='checkbox' placeholder="Compositor"/>
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
            <div>
                <div>
                    <div className='modal-bio-prof-infos-field'>
                        <span>Nationality</span>
                        <Field placeholder="Nationality"/>
                    </div>
                    <div className='modal-bio-prof-infos-field'>
                        <span>Website</span>
                        <Field placeholder="Website"/>
                    </div>
                </div>
                <div className='modal-bio-prof-infos-field'>
                    <span>Awards</span>
                    <Field placeholder="Awards"/>
                </div>
                <div className='modal-bio-prof-infos-field'>
                    <span>Awards</span>
                    <Field placeholder="Awards"/>
                </div>
            </div>
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
