import React, { useState, useMemo } from 'react';
import { createPortal } from 'react-dom';

import { ToastContext } from './ToastContext';
import { Toast } from '../../components/toast/Toast'

// Create a random ID
function generateUEID() {
    let first = (Math.random() * 46656) | 0;
    let second = (Math.random() * 46656) | 0;
    first = ('000' + first.toString(36)).slice(-3);
    second = ('000' + second.toString(36)).slice(-3);
  
    return first + second;
}

export const ToastProvider = (props) => {
    const [toasts, setToasts] = useState([]);
  
    const open = (content) => {
        const id = generateUEID();
        setToasts((currentToasts) => [
            ...currentToasts,
            { id: id, message: content.message, type: content.type },
        ]);
        setTimeout(() => {
            close(id);
        }, 5000);
    };

    const close = (id) => {
        setToasts((currentToasts) =>
        currentToasts.filter((toast) => toast.id !== id)
        );
    }

    const contextValue = useMemo(() => ({ open }), []);

    return (
        <ToastContext.Provider value={contextValue}>
        {props.children}

        {createPortal(
            <div className="toasts-wrapper">
            {toasts.map((toast) => (
                <Toast key={toast.id} message={toast.message} type={toast.type}/>
            ))}
            </div>,
            document.body
        )}
        </ToastContext.Provider>
    );
};