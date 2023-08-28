import React from 'react'

import './DashboardWorkAnalysis.css'
import Button from '../../button/Button';
import Field from '../../field/Field';

export const DashboardWorkAnalysis = (masterclassData) => {

    const [Learnings, setLearnings] = React.useState([]);
    const [tmpLearnings, setTmpLearnings] = React.useState('');

    return(
        <div className="dashboard-work-analysis">
            <div className='marg-bottom'>
                <Button size="long" type="button" label="Associate Masterclass" onClick={(e) => AssociateMasterclass(e)}/>
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
            <div className='modal-bio-prof-infos-field full-width'>
                <span className='marg-bottom'>Description</span>
                <Field placeholder="Piece by composer"/>
            </div>
            <div className='field-container2 marg-bottom'>
                <textarea className="modal-work-analysis-textarea" placeholder="..." row='10'/>
            </div>
        </div>
    );
}

export default DashboardWorkAnalysis;