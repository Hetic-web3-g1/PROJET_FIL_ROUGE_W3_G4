import React from 'react';
import PropTypes from 'prop-types';
import './Landing.css';
import Button from '../../components/button/Button';

export const Landing = ({ }) => {
  return (
    <div className="landing-wrap">
      <img
        className='landing-logo'
        srcset={`src/assets/Logo.svg`} >
      </img>
      <Button label="Enter" class="button button-primary padded" />
    </div>
  );
};

export default Landing;