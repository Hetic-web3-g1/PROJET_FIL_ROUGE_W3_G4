import React from 'react';
import PropTypes from 'prop-types';
import './Landing.css';
import Button from '../../components/button/Button';
import { Link } from "react-router-dom";

export const Landing = ({ }) => {
  return (
    <div className="landing-wrap">
      <img
        className='landing-logo'
        srcSet={`src/assets/Logo.svg`} >
      </img>
      <Link to="/login">
        <Button label="Enter" className="button button-primary padded"/>
      </Link>
    </div>
  );
};

export default Landing;