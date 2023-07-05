import React from 'react'
import propTypes from 'prop-types'

import Button from '../button/Button'
import Divider from '../divider/Divider'

import './modal.css'

export const Modal = ({ title, content, size, handleClose, handleSave }) => {
    return (
        <div className={(`modal modal-${size}`)}>
            <div className="modal-header">
                <h2 className='modal-title'>{title}</h2>
                <Divider />
            </div>
            <div className="modal-content">
                {content}
            </div>
            <div className="modal-footer">
                <Divider />
                <div className="modal-button-container">
                    <Button type="submit" primary={true} label="Save" onClick={handleSave}/>
                    <div className="modal-close-button">
                        <Button type="submit" primary={false} label="Close" onClick={handleClose}/>
                    </div>
                </div>
            </div>
        </div>
    );
}

Modal.propTypes = {
    title: propTypes.string,
    content: propTypes.object,
    handleClose: propTypes.func,
};

export default Modal;