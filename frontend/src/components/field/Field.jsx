import React, { useContext, useEffect, useState } from 'react';
import propTypes from 'prop-types';
import { useNavigate } from "react-router-dom";

import { ReactReduxContext } from 'react-redux';

import './field.css';
import OutsideAlerter from '../../utils/clickOutside';

export const Field = ({ type, placeholder, onChange, id, value }) => {
    const { store } = useContext(ReactReduxContext);
    const [searchData, setSearchData] = useState([]);
    const [noResult, setNoResult] = useState();
    const [noText, setNoText] = useState(true);
    const [timer, setTimer] = useState(null);
    const navigate = useNavigate();
  
    function HideAndShowPassword() {
        var x = document.getElementById(id);
        (x.type === "password") ? x.type = "text" : x.type = "password";
    }

    const userOptions = {
        method: 'GET',
        headers:  { 'Content-Type': 'application/json', 'accept': 'application/json', 'authorization': `${store.getState().user.user_token}` },
    };

    /**
     * Get value from click outside component and affect it to the noResult variable
     * @param {boolean} blockDisplayed Value to know if the HTML should be displayed
     */
    function handleDisplay(blockDisplayed) {
        setNoResult(blockDisplayed);
    }

    /**
     * On keyup make an API call to get the corresponding results
     * @param {string} currentSearch Current Search of the user
     */
    function onSearchChange(currentSearch) {
        setSearchData([]);
        clearTimeout(timer);
        currentSearch.target.value === '' ? setNoText(true) : setNoText(false);
        
        const requestSearch = setTimeout(() => 
        {
            currentSearch.target.value.length > 0 ? fetch(`http://${import.meta.env.VITE_API_ENDPOINT}/tags/search/${currentSearch.target.value}?tables=masterclass&tables=biography&tables=partition&tables=work_analysis`, userOptions)
                .then((response) => response.json())
                .then(data => {
                    setSearchData(data);
            })
            .catch((err) => {
                console.log('ERROR', err.message);
            }) : undefined
        }, 500)
        setTimer(requestSearch);
    }

    useEffect(() => {
        (searchData[0]?.length === 0 && searchData[1]?.length === 0 && searchData[2]?.length === 0 && searchData[3]?.length === 0) ? 
        setNoResult(true) : 
        setNoResult(false);
    }, [searchData]);

    return (
        <>
            <div className={['input-wrap', `input-wrap-${type}`].join(' ')}>
                <input
                    className={['field-input', `field-input-${type}`].join(' ')}
                    type={type}
                    placeholder={placeholder}
                    onChange={type === 'search' ? onSearchChange : (e) => onChange(e)}
                    id={id}
                    defaultChecked={false}
                    value={value}
                />
                <svg  
                    className={['field-icon', `field-icon-${type}`].join(' ')}
                    onClick={HideAndShowPassword}/>
            </div>
            <OutsideAlerter callback={handleDisplay}>
                <div style={{display: 'flex', justifyContent: 'center'}}>
                    
                    {!noResult &&                
                        <ul style={noText ? {display: 'none'} : null} className='results-block-searchable'>

                            <div style={searchData[0]?.length === 0 ? {display: 'none'} : undefined}>
                                <h2 className='title-search-category'>Masterclass</h2>
                                {searchData[0]?.map((el, index) => {return (<li onClick={() => (navigate(`/Masterclass/${el.id}`))} key={index} className='li-custom font'>{el.title}</li>)})}
                                <hr className='custom-search-hr' />
                            </div>

                            <div style={searchData[1]?.length === 0 ? {display: 'none'} : undefined}>
                                <h2 className='title-search-category'>Biography</h2>
                                {searchData[1]?.map((el, index) => {return (<li key={index} className='li-custom font'>{el.first_name}</li>)})}
                                <hr className='custom-search-hr' />
                            </div>

                            <div style={searchData[2]?.length === 0 ? {display: 'none'} : undefined}>
                                <h2 className='title-search-category'>Partition</h2>
                                {searchData[2]?.map((el, index) => {return (<li key={index} className='li-custom font'></li>)})}
                                <hr className='custom-search-hr' />
                            </div>

                            <div style={searchData[3]?.length === 0 ? {display: 'none'} : undefined}>
                                <h2 className='title-search-category'>Work Analysis</h2>
                                {searchData[3]?.map((el, index) => {return (<li key={index} className='li-custom font'>{el.title}</li>)})}
                                <hr className='custom-search-hr'/>
                            </div>
                        </ul>
                    }

                </div>
            </OutsideAlerter>
        </>
    );
}

Field.propTypes = {
    type: propTypes.string,
    placeholder: propTypes.string.isRequired,
    onChange: propTypes.func,
    image: propTypes.string,
};
Field.defaultProps = {
    type: 'text',
    placeholder: 'Placeholder',
    onChange: undefined,
};
export default Field;