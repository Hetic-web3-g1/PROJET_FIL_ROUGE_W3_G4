import React from 'react';
import PropTypes from 'prop-types';
import './Landing.css';
import Button from '../../components/button/Button';

export const Landing = ({ }) => {
  return (
    <div className="landing-wrap">
      <img
        className='landing-logo'
        srcSet={`src/assets/Logo.svg`} >
      </img>
      <Button label="Enter" className="button button-primary padded" />
    </div>
  );
};

export default Landing;