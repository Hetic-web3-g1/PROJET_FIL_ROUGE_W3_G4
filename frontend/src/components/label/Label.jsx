import React from 'react';
import PropTypes from 'prop-types';
import './Label.css';

export const Label = ({type, label, ...props }) => {
    return (
        <label
            type="label"
            className={['label', `label-${type}`].join(' ')}
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
};

Label.defaultProps = {
    type: null,
    label: 'Label',
    onClick: undefined,
};

export default Label;