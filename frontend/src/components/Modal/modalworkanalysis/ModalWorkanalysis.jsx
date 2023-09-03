import React from 'react'
import propTypes from 'prop-types'

import Modal from '../Modal'

import '../../professorfields/Professorfields.css'
import '../modalbioprof/ModalBioProf.css'
import './ModalWorkanalysis.css'
import Field from '../../field/Field'
import Button from '../../button/Button'
 

export const ModalWorkAnalysis = ({ handleClose, handleSave }) => {

    const [Learnings, setLearnings] = React.useState([]);
    const [tmpLearnings, setTmpLearnings] = React.useState('');
    const [about, setAbout] = React.useState('');
    const [content, setContent] = React.useState('');

    const AssociateMasterclass = (e) => {
        e.preventDefault();
    }   

    const masterclassContent = (
        <div className='modal-bio-prof-background-wrapper'>
            <div className='marg-bottom'>
            <Button size="long" type="button" label="Associate Masterclass" onClick={(e) => AssociateMasterclass(e)}/>
            </div>
            <div className='marg-bottom'>
            <Button size="long" type="button" primary='false' label="No Masterclass Associated"/>
            </div>
            <div className='field-container2 marg-bottom'>
                <span className='marg-bottom'>About this masterclass</span>
                <textarea className="modal-work-analysis-textarea" placeholder="..." row='10' onChange={(e) => setAbout(e.target.value)}/>
            </div>
   
            <div className='modal-bio-prof-infos-field full-width'>
            <span className='marg-bottom'>Learnings</span>
            {
                Learnings.map((learning, index) => {
                    return(
                        <div className='modal-bio-prof-award-field'>
                            <Field placeholder="Learning" value={learning} onChange={(e) => 
                                {
                                    let Array = [...Learnings];
                                    Array[index] = e.target.value;
                                    setLearnings(Array);
                                }
                            }/>
                        </div>
                    )
                })
            }
            </div>
            <div className='modal-bio-prof-infos-field full-width-flex'>
                <img src={'../../src/assets/plus.svg'} alt="plus" style={{marginRight: '1vw', cursor: 'pointer'}} onClick={() => setLearnings([...Learnings, tmpLearnings])}/>
                <Field placeholder="Learnings" onChange={(e) => setTmpLearnings([e.target.value])}/>
            </div>
            <div className='field-container2 marg-bottom'>
                <span className='marg-bottom'>Description</span>
                <textarea className="modal-work-analysis-textarea" placeholder="..." row='10' onChange={(e) => setContent(e.target.value)}/>
            </div>
        </div>
        
    );

    return(
        <Modal title="Work Analysis" content={masterclassContent} size='full' handleClose={handleClose} handleSave={handleSave} />
    );
};

ModalWorkAnalysis.propTypes = {
    handleClose: propTypes.func,
};

export default ModalWorkAnalysis;
