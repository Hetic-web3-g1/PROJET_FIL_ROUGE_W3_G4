import React from 'react';
import PropTypes from 'prop-types';
import './cardInstrument.css';

export const CardInstrument = ({ name, size, legend, onClick }) => {
  const mode = legend ? 'L-' : '';
  return (
    <div>
        <img className={`max-height`} height={size} src={`src/assets/cardInstrument/${mode}${name}.svg`} onClick={() => onClick(name)}/>
    </div>
  );
};

CardInstrument.propTypes = {
  name: PropTypes.string,
  legend: PropTypes.bool,
  size: PropTypes.number,
  onClick: PropTypes.func
};

CardInstrument.defaultProps = {
  name: 'Celio.svg',
  legend: false,
  size: 100
};

export default CardInstrument;