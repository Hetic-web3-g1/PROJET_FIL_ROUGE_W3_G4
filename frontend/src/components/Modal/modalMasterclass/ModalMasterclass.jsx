import React from 'react'
import propTypes from 'prop-types'

import Modal from '../Modal'
import CardInstrument from '../../cardInstrument/CardInstrument'

import './modalMasterclass.css'
import Instruments from '../../../constants/instruments'
import Field from '../../field/Field'
import Uploadcard from '../../upload/UploadCard'

export const ModalMasterClass = ({ biography, content, handleClose, handleSave }) => {

    const [instrument, setInstrument] = React.useState('');

    const handleInstrument = (instrument) => {
        setInstrument(instrument);
        console.log(instrument);
    };

    const masterclassContent = (
        <div className="modal-masterclass-content">
            <div className="modal-masterclass-infos">
                <div className="modal-masterclass-infos-1">
                    <div className="modal-masterclass-infos-field">
                        Composer
                        <Field placeholder="Composer"/>
                    </div>
                    <div className="modal-masterclass-infos-field">
                        Piece
                        <Field placeholder="Piece"/>
                    </div>
                    <div className="modal-masterclass-infos-element">
                        Professor
                        <Field placeholder="Professor"/>
                    </div>
                </div>
                <div className="modal-masterclass-infos-2">
                    <div className="modal-masterclass-infos-field">
                        Student
                        <Field placeholder="Student"/>
                    </div>
                    <div className="modal-masterclass-infos-field">
                        Producer
                        <Field placeholder="Producer"/>
                    </div>
                    <div className="modal-masterclass-infos-element">
                        Spoken Language
                        <Field placeholder="Spoken Language"/>
                    </div>
                </div>
            </div>
            <div className="modal-masterclass-instrument-wrapper">
                Instruments
                <div className="modal-masterclass-instrument">
                    {Instruments.map((instrument, index) => {
                        return (
                            <div className="instrument-card">
                                <CardInstrument key={`modal-instrument-card-${index}`} name={instrument} legend={true} onClick={handleInstrument}/>
                            </div>
                        )
                    })}
                </div>
            </div>
            <div className="modal-masterclass-background-wrapper">
                Background Image
                <div className="modal-masterclass-background-upload">
                    <Uploadcard/>
                </div>
            </div>
        </div>
    );

    return(
        <Modal title="Masterclass" content={masterclassContent} size='full' handleClose={handleClose} handleSave={handleSave} />
    );
};

ModalMasterClass.propTypes = {
    biography: propTypes.string,
    content: propTypes.string,
    handleClose: propTypes.func,
};

export default ModalMasterClass;
