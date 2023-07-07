import React, { useState } from 'react';
import PropTypes from 'prop-types';
import './cardInstrument.css';

export const CardInstrument = ({ name, size, legend, onClick }) => {
  const mode = legend ? 'L-' : '';
  const [style, setStyle] = useState(false);

  /**
   * Select all img element, replace the highlight by highlight-close class on all element to put the highlight class to the selected element.
   */
  function clickEvent() {
    document.querySelectorAll("img").forEach(e => e.classList.replace('highlight', 'highlight-close'));

    setStyle(!style);
    onClick(name);
  }

  return (
    <div>
        <img key={name} className={`img-card-instrument ${style ? 'highlight' : 'highlight-close'}`} height={size} id="first" src={`src/assets/cardInstrument/${mode}${name}.svg`} onClick={clickEvent}/>
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
  name: 'Celio',
  legend: false,
  size: 100
};

export default CardInstrument;