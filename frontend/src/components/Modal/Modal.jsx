import React from 'react'
import propTypes from 'prop-types'

import Button from '../button/Button'
import Divider from '../divider/Divider'

import './Modal.css'

export const Modal = ({ title, content, handleClose, handleSave }) => {
    return (
        <div className="modal">
            <div className="modal-header">
                <h2>{title}</h2>
                <Divider />
            </div>
            <div className="modal-content">
                {content}
            </div>
            <div>
                <Button type="submit" primary={true} label="Save" onClick={handleSave}/>
                <Button type="submit" primary={false} label="Close" onClick={handleClose}/>
            </div>
        </div>
    );
}

Modal.propTypes = {
    title: propTypes.string.isRequired,
    content: propTypes.string.isRequired,
    handleClose: propTypes.func.isRequired,
};

export default Modal;