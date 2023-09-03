import React from 'react';
import PropTypes from "prop-types";

import './Toast.css';
  
const SuccessIcon = () => (
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
      <path d="M256 512A256 256 0 1 0 256 0a256 256 0 1 0 0 512zM369 209L241 337c-9.4 9.4-24.6 9.4-33.9 0l-64-64c-9.4-9.4-9.4-24.6 0-33.9s24.6-9.4 33.9 0l47 47L335 175c9.4-9.4 24.6-9.4 33.9 0s9.4 24.6 0 33.9z" />
    </svg>
);

const FailureIcon = () => (
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
      <path d="M256 512A256 256 0 1 0 256 0a256 256 0 1 0 0 512zM175 175c9.4-9.4 24.6-9.4 33.9 0l47 47 47-47c9.4-9.4 24.6-9.4 33.9 0s9.4 24.6 0 33.9l-47 47 47 47c9.4 9.4 9.4 24.6 0 33.9s-24.6 9.4-33.9 0l-47-47-47 47c-9.4 9.4-24.6 9.4-33.9 0s-9.4-24.6 0-33.9l47-47-47-47c-9.4-9.4-9.4-24.6 0-33.9z" />
    </svg>
);

const WarningIcon = () => (
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
      <path d="M256 512A256 256 0 1 0 256 0a256 256 0 1 0 0 512zm0-384c13.3 0 24 10.7 24 24V264c0 13.3-10.7 24-24 24s-24-10.7-24-24V152c0-13.3 10.7-24 24-24zM224 352a32 32 0 1 1 64 0 32 32 0 1 1 -64 0z" />
    </svg>
);

export const Toast = ({message, type}) => {

    const iconMap = {
        success: <SuccessIcon />,
        failure: <FailureIcon />,
        warning: <WarningIcon />,
    };

    const toastIcon = iconMap[type] || null;

    return (
        <div className={`toast toast-${type}`} role="alert">
            <div className="toast-message">
                {toastIcon && (
                    <div className="icon">{toastIcon}</div>
                )}
                <p>{message}</p>
            </div>
        </div>
    );
}

Toast.defaultProps = {
    type: "success",
    message: "Success!",
};

Toast.propTypes = {
    type: PropTypes.string.isRequired,
    message: PropTypes.string.isRequired,
};

export default Toast;