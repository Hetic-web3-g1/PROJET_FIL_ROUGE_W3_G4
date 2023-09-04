import React, { useEffect, useState } from 'react';
import PropTypes from 'prop-types';
import './checkbox.css';
import { useSelector, ReactReduxContext } from 'react-redux';

export const Checkbox = ({ checkedByDefault, label, disabled, primary, value, returnValues }) => {

  const sortByStatusState = useSelector((state) => state.filters.filters.sort_by_status);
  const mode = primary ? 'checkbox-primary' : 'checkbox-secondary';
  const [checked, setChecked] = useState(checkedByDefault);

  function onCheck(event) {
    returnValues([event.target.value, event.target.checked])
    setChecked(event.target.checked)
  }

  useEffect(() => {
    if (sortByStatusState[0] === value && sortByStatusState[1] !== false) {
      setChecked(true); // to change because dont work with multiple check by the user
    }
  }, [])

  return (
    <div style={{marginTop: '10px'}}>
      <input value={value} disabled={disabled} checked={checked} onChange={(e) => onCheck(e)} type="checkbox" />
      <label className={mode} htmlFor="label">{label}</label>
    </div>
  );
};

Checkbox.propTypes = {
  disabled: PropTypes.bool,
  checkedByDefault: PropTypes.bool,
  label: PropTypes.string.isRequired,
  primary: PropTypes.bool,
  value: PropTypes.any,
  returnValues: PropTypes.array
};

Checkbox.defaultProps = {
  disabled: false,
  checkedByDefault: false,
  label: 'Label',
  primary: true,
  value: 'exemple'
};

export default Checkbox;