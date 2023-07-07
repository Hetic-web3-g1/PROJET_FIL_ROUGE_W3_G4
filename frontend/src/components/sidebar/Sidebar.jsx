import Checkbox from '../checkbox/Checkbox'
import Dropdown from '../dropdown/Dropdown'
import React, { useState } from 'react';
import './sidebar.css';

export const Sidebar = () => {
  const [open, setOpen] = useState(false);

  return (
    <div>
      <div style={open ? {display: 'none'} : null} className='sidebar-container'>

        <div className="sidebar-filters-container">
          <label className='sidebar-font'>Sort by:</label>
          <Dropdown/>

          <div className="sidebar-filter">
            <h1 className='sidebar-font'>Filters subtitle</h1>
            <Checkbox label='Filter' primary={false}/>
            <Checkbox label='Filter' primary={false}/>
            <Checkbox label='Filter' primary={false}/>
          </div>

          <div className="sidebar-filter">
            <h1 className='sidebar-font'>Filters subtitle</h1>
            <Checkbox label='Filter' primary={false}/>
            <Checkbox label='Filter' primary={false}/>
            <Checkbox label='Filter' primary={false}/>
            <Checkbox label='Filter' primary={false}/>
          </div>

          <div className="sidebar-filter">
            <h1 className='sidebar-font'>Filters subtitle</h1>
            <Checkbox label='Filter' primary={false}/>
            <Checkbox label='Filter' primary={false}/>
            <Checkbox label='Filter' primary={false}/>
          </div>

        </div>

        <div>
          <img onClick={() => setOpen(!open)} className='exit-sidebar-float' src="src\assets\sidebar\hide-sidebar.svg" alt="exit" />
        </div>
      </div>

      <div style={!open ? {display: 'none'} : null} className='small-sidebar'>
        <div>
          <img onClick={() => setOpen(!open)} className='exit-sidebar-float' src="src\assets\sidebar\show-sidebar.svg" alt="exit" />
        </div>
      </div>
    </div>
  );
};

export default Sidebar;