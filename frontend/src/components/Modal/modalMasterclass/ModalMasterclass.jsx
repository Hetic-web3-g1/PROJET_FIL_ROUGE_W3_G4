import react from 'React'
import propTypes from 'prop-types'

import Modal from '../Modal'
import CardInstrument from '../../cardInstrument/CardInstrument'

import './modalMasterClass.css'
import Instruments from '../../../constants/instruments'

export const ModalMasterClass = ({ biography, content, handleClose, handleSave }) => {

    const masterclassContent = (
        <div className="modal-masterclass-content">
            <div className="modal-masterclass-infos">
                <div className="modal-masterclass-infos-composer">
                </div>
                <div className="modal-masterclass-infos-piece">
                </div>
                <div className="modal-masterclass-infos-professor">
                </div>
                <div className="modal-masterclass-infos-student">
                </div>
                <div className="modal-masterclass-infos-producer">
                </div>
                <div className="modal-masterclass-infos-spokenLanguage">
                </div>
            </div>
            <div className="modal-masterclass-instrument">
                {Instruments.map((instrument, index) => {
                    return (
                        <CardInstrument key={index} name={instrument} legend={true}/>
                    )
                })}
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
