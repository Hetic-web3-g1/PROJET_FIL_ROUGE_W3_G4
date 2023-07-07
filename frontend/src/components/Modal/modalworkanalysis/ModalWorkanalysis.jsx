import React from 'react'
import propTypes from 'prop-types'

import Modal from '../Modal'

import '../../professorfields/Professorfields.css'
import '../modalbioprof/ModalBioprof.css'
import './ModalWorkanalysis.css'
import Field from '../../field/Field'
import Button from '../../button/Button'


export const ModalWorkanalysis = ({ biography, content, handleClose, handleSave }) => {

    const [instrument, setInstrument] = React.useState('');

    const handleInstrument = (instrument) => {
        setInstrument(instrument);
    };

    const masterclassContent = (
        <div className='modal-bio-prof-background-wrapper'>
            <div className='marg-bottom'>
            <Button size="long" type="button" label="Associate Masterclass"/>
            </div>
            <div className='marg-bottom'>
            <Button size="long" type="button" primary='false' label="No Masterclass Associated"/>
            </div>
            <div className='field-container2 marg-bottom'>
                <span className='marg-bottom'>About this masterclass</span>
                <textarea className="modal-work-analysis-textarea" placeholder="..." row='10'/>
            </div>
   
            <div className='modal-bio-prof-infos-field full-width'>
            <span className='marg-bottom'>Learnings</span>
            <Field placeholder="Learning"/>
            </div>
            <div className='modal-bio-prof-infos-field full-width-flex'>
                <img className='marg-right' src='src/assets/plus.svg'/> 
                <Field placeholder="Learning"/>
            </div>
            <div className='modal-bio-prof-infos-field full-width'>
            <span className='marg-bottom'>Description</span>
            <Field placeholder="Piece by composer"/>
            </div>
            <div className='field-container2 marg-bottom'>
                <textarea className="modal-work-analysis-textarea" placeholder="..." row='10'/>
            </div>
        </div>
        
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
