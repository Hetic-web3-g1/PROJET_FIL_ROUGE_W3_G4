import react from 'react';
import propTypes from 'prop-types';

import './field.css'

const searchIcon = '../../assets/search/search.svg';

export const Field = ({ type, placeholder, onChange, }) => {

function HideAndShowPassword () {
    var x = document.getElementsByClassName("field-input-password")[0]; 
    if (x.type === "password") {
        x.type = "text";
    } else {
        x.type = "password";
    }}


    return (
        <div className='input-wrap'>
            <input
                className={['field-input', `field-input-${type}`].join(' ')}
                type={type}
                placeholder={placeholder}
                onChange={onChange}
            />
            <svg  
                className={['field-icon', `field-icon-${type}`].join(' ')}
                onClick={HideAndShowPassword}
                />
        </div>
    );
}


Field.propTypes = {
    type: propTypes.string,
    placeholder: propTypes.string.isRequired,
    onChange: propTypes.func,
    image: propTypes.string,
};

Field.defaultProps = {
    type: 'text',
    placeholder: 'Placeholder',
    onChange: undefined,
};

export default Field;


