import React from 'react'
import propTypes from 'prop-types'


import Modal from '../Modal'
import CardInstrument from '../../cardInstrument/CardInstrument'

import './ModalCreateMasterclass.css'
import Instruments from '../../../constants/instruments'
import Field from '../../field/Field'
import Uploadcard from '../../upload/UploadCard'


export const ModalCreateMasterclass = ({ biography, content, handleClose, handleSave}) => {


    const [instrument, setInstrument] = React.useState('');

    const handleInstrument = (instrument) => {
        setInstrument(instrument);
    };



    const bioContent = (
        <div className="modal-bio-prof-content">
            <div className="modal-bio-prof-infos">
                <div className="modal-bio-prof-infos-1">
                <div className="flexx">
                    <div className="modal-bio-prof-infos-field marg-right">
                        Composer
                        <Field placeholder="Composer"/>
                    </div>
                    <div className="modal-bio-prof-infos-field marg-right">
                        Piece
                        <Field placeholder="Piece"/>
                    </div>
                </div>
                <div className="flexx">
                    <div className="modal-bio-prof-infos-field marg-right">
                        Professor
                        <Field placeholder="Professor"/>
                    </div>
                    <div className="modal-bio-prof-infos-field marg-right">
                        Student
                        <Field placeholder="Student"/>
                    </div>
                </div>
                <div className="flexx">
                    <div className="modal-bio-prof-infos-field marg-right">
                        Producer
                        <Field placeholder="Producer"/>
                    </div>
                    <div className="modal-bio-prof-infos-field marg-right">
                        Spoken Language
                        <Field placeholder="Spoken Language"/>
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
            <div className="modal-bio-prof-background-wrapper">
                        <span className='center'>Background Image</span>
                            <div className="modal-bio-prof-background-upload">
                                <Uploadcard/>
                            </div>
            </div>
        </div>
    );

    return(
        <Modal title="Biography" content={bioContent} size='full' handleClose={handleClose} handleSave={handleSave} />
    );
};

ModalCreateMasterclass.propTypes = {
    biography: propTypes.string,
    content: propTypes.string,
    handleClose: propTypes.func,
};

export default ModalCreateMasterclass;
