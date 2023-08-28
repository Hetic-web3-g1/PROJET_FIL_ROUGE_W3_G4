import React from 'react'

import './DashboardWorkAnalysis.css'
import Button from '../../button/Button';
import Field from '../../field/Field';

export const DashboardWorkAnalysis = () => {
    return(
        <div className="dashboard-work-analysis">
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
                    <img className='marg-right' src='../src/assets/plus.svg'/> 
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
}

export default DashboardWorkAnalysis;