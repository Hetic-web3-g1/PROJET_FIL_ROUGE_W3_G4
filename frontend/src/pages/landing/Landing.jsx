import React from 'react';
import PropTypes from 'prop-types';
import './Landing.css';
import Button from '../../components/button/Button';

export const Landing = ({ }) => {
  // const mode = legend ? 'L-' : '';
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

// CardInstrument.propTypes = {
//   name: PropTypes.string,
//   legend: PropTypes.bool,
//   size: PropTypes.number
// };

// CardInstrument.defaultProps = {
//   name: 'Celio.svg',
//   legend: false,
//   size: 100
// };

export default Landing;