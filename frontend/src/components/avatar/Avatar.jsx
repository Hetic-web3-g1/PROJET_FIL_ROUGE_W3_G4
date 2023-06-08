import React from 'react';
import PropTypes from 'prop-types';
import './avatar.css';

export const Avatar = ({ onClick }) => {
  return (
    <div onClick={onClick}>
        <img className='image-style' src="src\assets\linkPlaceholder.png" alt="placeholder" />
    </div>
  );
};

Avatar.propTypes = {
  onClick: PropTypes.func
};

export default Avatar;