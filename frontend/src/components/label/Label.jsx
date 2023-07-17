import React from 'react';
import PropTypes from 'prop-types';
import './Label.css';

export const Label = ({type, label, log, ...props }) => {
    return (
        <label
            type="label"
            className={['label', `label-${type}`, `label-${log}`].join(' ')}
            {...props}
            >
            {label}
        </label>
    );
    };

Label.propTypes = {
    type: PropTypes.string,
    label: PropTypes.string.isRequired,
    onClick: PropTypes.func,
    log: PropTypes.string,
};

Label.defaultProps = {
    type: null,
    label: 'Label',
    onClick: undefined,
    log: null,
};

export default Label;