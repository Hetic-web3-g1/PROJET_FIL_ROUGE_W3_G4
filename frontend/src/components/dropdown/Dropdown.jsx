import React, { useState } from 'react';
import PropTypes from 'prop-types';
import './Dropdown.css';

export const Dropdown = ({ options, callback, disabled, defaultValue }) => {
  const [open, setOpen] = useState(false);
  const [selectedItem, setSelectedItem] = useState(defaultValue);
  const mode = disabled ? 'dropdown-disabled' : '';
  const isOpen = open ? 'open-chevron-svg' : 'close-chevron-svg';

  /**
   * Close the dropdown, set the name of the dropdown and emit the value to the parent
   * @param {string} item Selected item in the dropdown
   */
  function selectItem(item) {
    setOpen(!open);
    setSelectedItem(item);
    callback(item);
  }

  return (
    <div>
      <div style={disabled ? {pointerEvents: 'none', backgroundColor: '#F7F7F7'} : null} onClick={() => setOpen(!open)} className='no-select div-dropdown font'>
        <span className={mode}>{selectedItem}</span>
        <img className={`${mode} ${isOpen}`} src="../src\assets\dropdown\Chevron.svg" alt="chevron" />
      </div>

      {open && <ul className='no-select ul-custom'>
        {options.map((el, index) => <li onClick={() => selectItem(el)} className='li-custom font' key={index}>{el}</li>)}
      </ul>}
    </div>
  );
};

Dropdown.propTypes = {
  options: PropTypes.arrayOf(PropTypes.string),
  callback: PropTypes.func.isRequired, // Callback function needed in parent component to get the value of the dropdown
  disabled: PropTypes.bool,
  defaultValue: PropTypes.string
};

Dropdown.defaultProps = {
  options: ['Option 1', 'Option 2', 'Option 3', 'Option 4', 'Option 5'],
  disabled: false
};

export default Dropdown;