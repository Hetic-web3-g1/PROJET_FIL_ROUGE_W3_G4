import React from 'react';
import PropTypes from 'prop-types';
import './button.css';

export const Button = ({ primary, type, backgroundColor, size, label, ...props }) => {
  const mode = primary ? 'button-secondary' : 'button-primary';
  return (
    <button
      type={type}
      className={['button', `button-${size}`, mode].join(' ')}
      style={backgroundColor && { backgroundColor }}
      {...props}
    >
      {label}
    </button>
  );
};

Button.propTypes = {
  primary: PropTypes.bool,
  type: PropTypes.oneOf(['button', 'submit', 'reset']),
  backgroundColor: PropTypes.string,
  size: PropTypes.oneOf(['small', 'medium', 'large', 'long']),
  label: PropTypes.string.isRequired,
  onClick: PropTypes.func,
};

Button.defaultProps = {
  type: 'button',
  backgroundColor: null,
  primary: false,
  size: 'medium',
  onClick: undefined,
};

export default Button;