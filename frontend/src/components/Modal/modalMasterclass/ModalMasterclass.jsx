import React from 'react'
import propTypes from 'prop-types'

import Modal from '../Modal'
import CardInstrument from '../../cardInstrument/CardInstrument'

import './modalMasterclass.css'
import Instruments from '../../../constants/instruments'
import Field from '../../field/Field'
import Uploadcard from '../../upload/UploadCard'

export const ModalMasterClass = ({ handleClose, store }) => {

    const [instrument, setInstrument] = React.useState('');
    const [composer, setComposer] = React.useState('');
    const [piece, setPiece] = React.useState('');
    const [professor, setProfessor] = React.useState('');
    const [description, setDescription] = React.useState('');
    const [title, setTitle] = React.useState('');

    const createdBy = store.getState().user.profile.id;
    const academyId = store.getState().user.profile.academy_id;

    const handleInstrument = (instrument) => {
        setInstrument([instrument]);
    };

    const handleSave = () => {
        const masterclassOptions = {
            method: 'POST',
            headers: { 'Content-Type': 'application/json', 'accept': 'application/json', 'authorization': `${store.getState().user.user_token}` },
            body: JSON.stringify({
                academy_id: academyId,
                title: title,
                description: description,
                //teacher_bio_id: professor,
                //composer_bio_id: composer,
                //partition_id: piece,
                instrument: instrument,
                created_by: createdBy,
            }),
        };
        fetch(`http://localhost:4000/masterclasses/masterclass`, masterclassOptions).then((response) => response.json()).then(data => {
            if (data?.detail[0].msg != "field required") {
                handleClose();
            } else {
                alert('Invalid data');
            }
        });
    };

    const masterclassContent = (
        <form className="modal-masterclass-content">
            <div className="modal-masterclass-infos">
                <div className="modal-masterclass-infos-1">
                    <div className="modal-masterclass-infos-field">
                        Title
                        <Field placeholder="Title" onChange={(e) => setTitle(e.target.value)}/>
                    </div>
                    <div className="modal-masterclass-infos-field">
                        Partition
                        <Field placeholder="Piece"/>
                    </div>
                    <div className="modal-masterclass-infos-field">
                        Professor
                        <Field placeholder="Professor"/>
                    </div>
                    <div className="modal-masterclass-infos-field">
                        Composer
                        <Field placeholder="Student"/>
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
            <div style={{ display: 'flex','flex-direction': 'column'}}>
                <span>Description</span>
                <textarea className="modal-bio-prof-textarea" placeholder="..." row='20' onChange={(e) => setDescription(e.target.value)}/>
            </div>
        </form>
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
