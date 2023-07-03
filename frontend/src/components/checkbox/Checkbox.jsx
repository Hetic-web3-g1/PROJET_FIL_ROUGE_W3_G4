import React, { useState } from 'react';
import PropTypes from 'prop-types';
import './checkbox.css';

export const Checkbox = ({ checkedByDefault, label, disabled, primary }) => {
  const [checked, setChecked] = useState(checkedByDefault);
  const mode = primary ? 'checkbox-primary' : 'checkbox-secondary';
  return (
    <div style={{marginTop: '10px'}}>
      <input disabled={disabled} checked={checked} onChange={(e) => setChecked(e.target.checked)} type="checkbox" />
      <label className={mode} for="label">{label}</label>
    </div>
  );
};

Checkbox.propTypes = {
  disabled: PropTypes.bool,
  checkedByDefault: PropTypes.bool,
  label: PropTypes.string.isRequired,
  primary: PropTypes.bool
};

Checkbox.defaultProps = {
  disabled: false,
  checkedByDefault: false,
  label: 'Label',
  primary: true
};

export default Checkbox;