import React from 'react';
import PropTypes from 'prop-types';
import './cardInstrument.css';

export const CardInstrument = ({ name, size }) => {
  return (
    <div>
        <img className='max-height' height={size} src={`src/assets/cardInstrument/${name}`} />
    </div>
  );
};

CardInstrument.propTypes = {
    name: PropTypes.string,
    with: PropTypes.number
};

CardInstrument.defaultProps = {
    name: 'Celio.svg',
    size: 100
};

export default CardInstrument;