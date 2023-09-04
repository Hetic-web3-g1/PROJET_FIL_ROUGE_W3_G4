import Checkbox from '../checkbox/Checkbox'
import Dropdown from '../dropdown/Dropdown'
import { useDispatch, ReactReduxContext, useSelector } from 'react-redux';
import PropTypes from 'prop-types';
import React, { useContext, useEffect, useState } from 'react';
import './Sidebar.css';
import { FiltersActions } from '../../features/actions/filters';

export const Sidebar = ({categories}) => {
  const [open, setOpen] = useState(false);
  const [checkboxList, setCheckboxList] = useState([]);
  const customFilters = ['Created at', 'Last update'];
  const dispatch = useDispatch();
  const {store} = useContext(ReactReduxContext);
  // const sortByStatusState = useSelector((state) => state.filters.filters.sort_by_status);


  function handleValueDropdown(childData) {
    dispatch(FiltersActions.sortBy(childData));
  }

  function handleCheckboxTrue(event) {
    setCheckboxList(values => [...values, event]);
  }

  function handleCheckboxFalse(event) {
    const index = checkboxList.findIndex(e => e[0] === event[0]);
    var tmp = checkboxList;
    console.log('before', tmp);
    tmp.splice(index, 1);
    console.log('after', tmp);
    setCheckboxList(tmp);
  }

  useEffect(() => {
    dispatch(FiltersActions.sortByStatus(checkboxList));
  }, [checkboxList])

  return (
    <div>
      <div style={open ? {display: 'none'} : null} className='sidebar-container'>

        <div className="sidebar-filters-container">
          <label className='sidebar-font'>Sort by:</label>
          <Dropdown returnValues={handleValueDropdown} options={customFilters} defaultValue={store.getState().filters.filters.sort_by}/>

          {
            Object.keys(categories).map((categoryTitle) => {
              { 
                return(
                  <div className="sidebar-filter">
                    <h1 className='sidebar-font'>{categoryTitle}</h1>
                    {
                      categories[categoryTitle].map(filterTitle => { return(<Checkbox returnValues={(e) => e[1] === true ? handleCheckboxTrue(e) : handleCheckboxFalse(e)} value={filterTitle} label={filterTitle} primary={false}/>) })
                    }
                  </div>
                )
              }
            })
          }

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

Sidebar.propTypes = {
  options: PropTypes.objectOf(PropTypes.array).isRequired,
};

Sidebar.defaultProps = {
  options: {Title1: ['Cat1Filter1', 'Cat1Filter2', 'Cat1Filter3'], Title2: ['Cat2Filter1', 'Cat2Filter2', 'Cat2Filter3'], Title3: ['Cat3Filter1', 'Cat3Filter2', 'Cat3Filter3']},
};

export default Sidebar;