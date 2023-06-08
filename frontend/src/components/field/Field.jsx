import React from 'react';
import propTypes from 'prop-types';

import './field.css'

const searchIcon = '../../assets/search/search.svg';

export const Field = ({ type, placeholder, onChange }) => {
    return (
        <input
            className={['field-input', `field-input-${type}`].join(' ')}
            type={type}
            placeholder={placeholder}
            onChange={onChange}
        />
    );
}

Field.propTypes = {
    type: propTypes.string,
    placeholder: propTypes.string.isRequired,
    onChange: propTypes.func,
};

Field.defaultProps = {
    type: 'text',
    placeholder: 'Placeholder',
    onChange: undefined,
};

export default Field;
