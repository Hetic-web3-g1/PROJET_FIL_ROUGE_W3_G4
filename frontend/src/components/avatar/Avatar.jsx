import React from 'react';
import PropTypes from 'prop-types';
import './avatar.css';

export const Avatar = ({ onClick, size }) => {
  return (
    <div onClick={onClick}>
        <img style={{height: size}} className='image-style' src="../src\assets\kirbok.jpg" alt="placeholder" />
    </div>
  );
};

Avatar.propTypes = {
  onClick: PropTypes.func,
  size: PropTypes.string
};

Avatar.defaultProps = {
  size: '60px'
};

export default Avatar;