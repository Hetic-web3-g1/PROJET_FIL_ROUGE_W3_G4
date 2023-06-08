import React, { useState } from 'react';
import PropTypes from 'prop-types';
import './sidebar.css';

export const Sidebar = ({ name, size, legend, onClick }) => {

  return (
    <div>
    </div>
  );
};

Sidebar.propTypes = {
  name: PropTypes.string,
  legend: PropTypes.bool,
  size: PropTypes.number,
  onClick: PropTypes.func
};

Sidebar.defaultProps = {
  name: 'Celio',
  legend: false,
  size: 100
};

export default Sidebar;