import react from 'React'
import propTypes from 'prop-types'

import Modal from '../Modal'

import './modalMasterClass.css'

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
