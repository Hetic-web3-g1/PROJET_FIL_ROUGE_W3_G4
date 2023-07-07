import React from 'react'
import propTypes from 'prop-types'

import Modal from '../Modal'
import CardInstrument from '../../cardInstrument/CardInstrument'

import './ModalWorkanalysis.css'
import Instruments from '../../../constants/instruments'
import Field from '../../field/Field'
import Uploadcard from '../../upload/UploadCard'
import Button from '../../button/Button'
import Divider from '../../divider/Divider'
import Label from '../../label/Label'

export const ModalWorkanalysis = ({ biography, content, handleClose, handleSave }) => {

    const [instrument, setInstrument] = React.useState('');

    const handleInstrument = (instrument) => {
        setInstrument(instrument);
    };

    const masterclassContent = (
        <div className='modal-work-analysis'>
            <div className='button-container'>
            <Button size="long" type="button" label="Associate Masterclass"/>
            </div>
            <div className='button-container'>
            <Button size="long" type="button" primary='false' label="No Masterclass Associated"/>
            </div>
            <div class>
                <span>About this masterclass</span>
                <Field placeholder="..."/>
            </div>
        </div>
        // <div className="modal-masterclass-content">
        //     <div className="modal-masterclass-infos">
        //         <div className="modal-masterclass-infos-1">
        //             <div className="modal-masterclass-infos-field">
        //                 Composer
        //                 <Field placeholder="Composer"/>
        //             </div>
        //             <div className="modal-masterclass-infos-field">
        //                 Piece
        //                 <Field placeholder="Piece"/>
        //             </div>
        //             <div className="modal-masterclass-infos-element">
        //                 Professor
        //                 <Field placeholder="Professor"/>
        //             </div>
        //         </div>
        //         <div className="modal-masterclass-infos-2">
        //             <div className="modal-masterclass-infos-field">
        //                 Student
        //                 <Field placeholder="Student"/>
        //             </div>
        //             <div className="modal-masterclass-infos-field">
        //                 Producer
        //                 <Field placeholder="Producer"/>
        //             </div>
        //             <div className="modal-masterclass-infos-element">
        //                 Spoken Language
        //                 <Field placeholder="Spoken Language"/>
        //             </div>
        //         </div>
        //     </div>
        //     <div className="modal-masterclass-instrument-wrapper">
        //         Instruments
        //         <div className="modal-masterclass-instrument">
        //             {Instruments.map((instrument, index) => {
        //                 return (
        //                     <div className="instrument-card">
        //                         <CardInstrument key={`modal-instrument-card-${index}`} name={instrument} legend={true} onClick={handleInstrument}/>
        //                     </div>
        //                 )
        //             })}
        //         </div>
        //     </div>
        //     <div className="modal-masterclass-background-wrapper">
        //         Background Image
        //         <div className="modal-masterclass-background-upload">
        //             <Uploadcard/>
        //         </div>
        //     </div>
        // </div>
    );

    return(
        <Modal title="Work Analysis" content={masterclassContent} size='full' handleClose={handleClose} handleSave={handleSave} />
    );
};

ModalWorkanalysis.propTypes = {
    biography: propTypes.string,
    content: propTypes.string,
    handleClose: propTypes.func,
};

export default ModalWorkanalysis;
