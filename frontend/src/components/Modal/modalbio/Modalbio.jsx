import React from 'react'
import propTypes from 'prop-types'

import Modal from '../Modal'
import CardInstrument from '../../cardInstrument/CardInstrument'

import './modalbio.css'
import Instruments from '../../../constants/instruments'
import Field from '../../field/Field'
import Uploadcard from '../../upload/UploadCard'

export const ModalBio = ({ biography, content, handleClose, handleSave }) => {

    const [instrument, setInstrument] = React.useState('');

    const handleInstrument = (instrument) => {
        setInstrument(instrument);
    };

    const bioContent = (
        <div className="modal-bio-content">
            <div className="modal-bio-infos">
                <div className="modal-bio-infos-1">
                    <div className="modal-bio-infos-field">
                        First Name
                        <Field placeholder="First Name"/>
                    </div>
                    <div className="modal-bio-infos-field">
                        Last Name
                        <Field placeholder="Last Name"/>
                    </div>
                    <div className="modal-bio-infos-checkbox">
                        <div className="modal-bio-infos-element">
                            <Field type='checkbox' placeholder="Professor"/>
                            <span>Professor</span>

                        </div>
                        <div className="modal-bio-infos-element">
                            <Field type='checkbox' placeholder="Compositor"/>
                            <span>Compositor</span>

                        </div>
                    </div>
                    {/* <div className='upload-avatar'>
                        <input type="file" id="avatar" name="avatar" accept="image/png, image/jpeg"/>
                    </div> */}
                        <div className="modal-bio-background-wrapper">
                        <span>Avatar</span>
                            <div className="modal-bio-background-upload">
                                <Uploadcard/>
                            </div>
                        </div>
                </div>

            </div>
            <div className="modal-bio-instrument-wrapper">
                Instruments
                <div className="modal-bio-instrument">
                    {Instruments.map((instrument, index) => {
                        return (
                            <div className="instrument-card">
                                <CardInstrument key={`modal-instrument-card-${index}`} name={instrument} legend={true} onClick={handleInstrument}/>
                            </div>
                        )
                    })}
                </div>
            </div>
            <div style={{ display: 'flex','flex-direction': 'column'}}>
                <span>Biography</span>
                {/* <Field type="bio" placeholder='...'/> */}
                <textarea className="modal-bio-textarea" placeholder="..." row='20'/>
            </div>
        </div>
    );

    return(
        <Modal title="Biography" content={bioContent} size='full' handleClose={handleClose} handleSave={handleSave} />
    );
};

ModalBio.propTypes = {
    biography: propTypes.string,
    content: propTypes.string,
    handleClose: propTypes.func,
};

export default ModalBio;
