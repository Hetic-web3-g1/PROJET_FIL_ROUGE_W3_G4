import React, { useState, useContext } from 'react'
import { ReactReduxContext } from 'react-redux'
import { useToast } from '../../../utils/toast';

import './DashboardWorkAnalysis.css'
import Button from '../../button/Button';
import Field from '../../field/Field';

export const DashboardWorkAnalysis = ({masterclassData, handleSave, workAnalysisData}) => {

    const toast = useToast();
    const { store } = useContext(ReactReduxContext)

    const [Learnings, setLearnings] = useState(workAnalysisData?.learning ? workAnalysisData?.learning : []);
    const [tmpLearnings, setTmpLearnings] = useState('');
    const [About, setAbout] = useState(workAnalysisData?.about);
    const [Description, setDescription] = useState(workAnalysisData?.content);

    const WorkAnalysisJoin = (id) => {
        var newMasterclassData = masterclassData
        newMasterclassData.work_analysis_id = id
        newMasterclassData.updated_by = store?.getState().user.user_id
        newMasterclassData.updated_at = new Date()
        handleSave(newMasterclassData)
    }

    const SaveWorkAnalysis = (e) => {
        e.preventDefault();
        var route = masterclassData?.work_analysis_id !== null  ? `work_analyzes/work_analysis/${masterclassData?.work_analysis_id}` : `work_analyzes/work_analysis`
        var method = masterclassData?.work_analysis_id !== null  ? 'PUT' : 'POST'
        const options = {
            method: method,
            headers: { 'Content-Type': 'application/json', 'accept': 'application/json', 'authorization': `${store.getState().user.user_token}` },
            body: JSON.stringify({
                title: masterclassData.title,
                about: About,
                content: Description,
                learning: Learnings,
                status: "created"
            }),
        };
        fetch(`http://${import.meta.env.VITE_API_ENDPOINT}/${route}`, options).then((response) => response.json()).then(data => {
            masterclassData?.work_analysis_id == null ? WorkAnalysisJoin(data) : toast.open({message: 'Work Analysis saved', type: 'success'});
        });
    }

    return(
        <div className="dashboard-work-analysis">
            <form>
                <div className='field-container2 marg-bottom'>
                    <span className='marg-bottom'>About this masterclass</span>
                    <textarea className="modal-work-analysis-textarea" placeholder="..." value={About} row='10' onChange={(e) => setAbout(e.target.value)}/>
                </div>
                <div className='modal-bio-prof-infos-field full-width'>
                    <span className='marg-bottom'>Learnings</span>
                    {
                        Learnings?.map((learning, index) => {
                            return(
                                <div className='modal-bio-prof-award-field'>
                                    <Field placeholder="Learning" value={learning} onChange={(e) => 
                                        {
                                            let Array = [...Learnings];
                                            Array[index] = e.target.value;
                                            setLearnings(Array);
                                        }}
                                    />
                                </div>
                            )
                        })
                    }
                </div>
                <div className='modal-bio-prof-infos-field full-width-flex'>
                    <img src={'../../src/assets/plus.svg'} alt="plus" style={{marginRight: '1vw', cursor: 'pointer'}} onClick={() => setLearnings([...Learnings, tmpLearnings])}/>
                    <Field placeholder="Learnings" onChange={(e) => setTmpLearnings(e.target.value)}/>
                </div>
                <div className='field-container2 marg-bottom'>
                    <span className='marg-bottom'>Content description</span>
                    <textarea className="modal-work-analysis-textarea" placeholder="..." value={Description} row='10' onChange={(e) => setDescription(e.target.value)}/>
                </div>
            </form>
            <div className='marg-bottom'>
                <Button size="long" type="button" label="Save work analysis" onClick={(e) => SaveWorkAnalysis(e)}/>
            </div>
        </div>
    );
}

export default DashboardWorkAnalysis;