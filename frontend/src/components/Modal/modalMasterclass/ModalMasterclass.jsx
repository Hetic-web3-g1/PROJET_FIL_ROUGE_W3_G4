import react from 'React'
import propTypes from 'prop-types'

import Modal from '../Modal'
import CardInstrument from '../../cardInstrument/CardInstrument'

import './modalMasterclass.css'
import Instruments from '../../../constants/instruments'
import Field from '../../field/Field'
import Uploadcard from '../../upload/UploadCard'

export const ModalMasterClass = ({ biography, content, handleClose, handleSave }) => {

    const masterclassContent = (
        <div className="modal-masterclass-content">
            <div className="modal-masterclass-infos">
                <div className="modal-masterclass-infos-1">
                    <div className="modal-masterclass-infos-composer">
                        Composer
                        <Field placeholder="Composer"/>
                    </div>
                    <div className="modal-masterclass-infos-piece">
                        Piece
                        <Field placeholder="Piece"/>
                    </div>
                    <div className="modal-masterclass-infos-professor">
                        Professor
                        <Field placeholder="Professor"/>
                    </div>
                </div>
                <div className="modal-masterclass-infos-2">
                    <div className="modal-masterclass-infos-student">
                        Student
                        <Field placeholder="Student"/>
                    </div>
                    <div className="modal-masterclass-infos-producer">
                        Producer
                        <Field placeholder="Producer"/>
                    </div>
                    <div className="modal-masterclass-infos-spokenLanguage">
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
                            <CardInstrument key={index} name={instrument} legend={true}/>
                        )
                    })}
                </div>
            </div>
            <div className="modal-masterclass-background-wrapper">
                Background Image
                <div className="modal-masterclass-background-upload">
                    <Uploadcard />
                </div>
            </div>
        </div>
    );

    return(
        <Modal title="Masterclass" content={masterclassContent} size='full' handleClose={handleClose} handleSave={handleSave} />
    );
};

ModalMasterClass.propTypes = {
    biography: propTypes.string.isRequired,
    content: propTypes.string.isRequired,
    handleClose: propTypes.func.isRequired,
};

export default ModalMasterClass;
