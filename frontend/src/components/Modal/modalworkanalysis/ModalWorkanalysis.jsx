import React from 'react'
import propTypes from 'prop-types'

import Modal from '../Modal'

import '../../professorfields/Professorfields.css'
import '../modalbioprof/ModalBioProf.css'
import './ModalWorkanalysis.css'
import Field from '../../field/Field'
import Button from '../../button/Button'
 

export const ModalWorkAnalysis = ({ handleClose, store, DefaultValue }) => {

    const [tmpLearnings, setTmpLearnings] = React.useState('');
    const [learnings, setLearnings] = React.useState(DefaultValue.learning || []);
    const [about, setAbout] = React.useState(DefaultValue.about || '');
    const [content, setContent] = React.useState(DefaultValue.content || '');
    const [awards, setAwards] = React.useState([]);
    const [title, setTitle] = React.useState(DefaultValue.title || '');
    // const [learning, setLearning] = React.useState(DefaultValue.learning || []);


    const handleSave = () => {
        const workAnalysisOptions = {
          method: 'POST',
          headers: { 'Content-Type': 'application/json', 'accept': 'application/json', 'authorization': `${store.getState().user.user_token}` },
          body : JSON.stringify({
                title: title,
                about: about,
                learning: learnings,
                content: content,
                award: awards,
            }),
        };
        fetch(`http://${import.meta.env.VITE_API_ENDPOINT}/work_analyzes/work_analysis`, workAnalysisOptions).then((response) => response.json()).then(data => {
          if (data?.detail[0].msg != "field required") {
            handleClose();
          } else {
            alert('Invalid data');
          }
        });


    };

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
                <textarea value={about} className="modal-work-analysis-textarea" placeholder='...' row='10' onChange={(e) => setAbout(e.target.value)}/>
            </div>
   
            <div className='modal-bio-prof-infos-field full-width'>
            <span className='marg-bottom'>Learnings</span>
            {
                learnings.map((learning, index) => {
                    return(
                        <div className='modal-bio-prof-award-field'>
                            <Field placeholder="Learning" value={learning} onChange={(e) => 
                                {
                                    let Array = [...learnings];
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
                <img src={'../../src/assets/plus.svg'} alt="plus" style={{marginRight: '1vw', cursor: 'pointer'}} onClick={() => setLearnings([...learnings, tmpLearnings])}/>
                <Field placeholder="Learnings" onChange={(e) => setTmpLearnings([e.target.value])}/>
            </div>
            <div className='field-container2 marg-bottom'>
                <span className='marg-bottom'>Piece by composer</span>
                <textarea value={content} className="modal-work-analysis-textarea" placeholder="..." row='10' onChange={(e) => setContent(e.target.value)}/>
            </div>
        </div>
        
    );

    return(
        <Modal title="Work Analysis" content={masterclassContent} size='full' handleClose={handleClose} handleSave={handleSave} />
    );
};

ModalWorkAnalysis.propTypes = {
    
    content: propTypes.string,
    handleClose: propTypes.func,
};

export default ModalWorkAnalysis;
