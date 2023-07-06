import React from 'react';
import PropTypes from 'prop-types';
import './Tabs.css';

export const Tabs = ({ callback, tabActiveByDefault }) => {
  const tabsName = [
    {name: 'Masterclass', isActive: false},
    {name: 'Team', isActive: false},
    {name: 'Video', isActive: false},
    {name: 'Partition', isActive: false},
    {name: 'Work analysis', isActive: false},
    {name: 'Professor', isActive: false},
    {name: 'Compositor', isActive: false},
  ];

  tabsName.forEach(e => {
    if (e.name === tabActiveByDefault) {
      e.isActive = true;
    }
  })

  /**
   * Remove the active class of all li element to set this to the selected one and emit the tab name to the parent element
   * @param {HTMLElement} selectedTabHTML HTML element of the selected tab
   * @param {string} currentTab Current tab name
   */
  function handleTabs(selectedTabHTML, currentTab) {
    document.querySelector(".custom-tabs-li").forEach(e => e.classList.remove('active'));
    selectedTabHTML.classList.add('active');
    callback(currentTab);
  }

  return (
    <div>
        <ul className='tabs-ul'>
          {tabsName.map((tab, index) =>
          <li onClick={(e) => handleTabs(e.target, tab.name)} key={index} className={`${tab.isActive === true ? 'active' : ''} custom-tabs-li no-select`}>{tab.name}</li>
          )}
        </ul>
    </div>
  );
};

Tabs.propTypes = {
  callback: PropTypes.func.isRequired, // Callback function needed in parent component to get the value of the Tabs
  tabActiveByDefault: PropTypes.string
};

Tabs.defaultProps = {
  tabActiveByDefault: 'Masterclass'
};

export default Tabs;