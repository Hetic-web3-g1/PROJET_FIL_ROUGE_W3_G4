import React, { useEffect, useContext, useState } from 'react';
import { useNavigate } from "react-router-dom";
import propTypes from 'prop-types';

import { useSelector, ReactReduxContext } from 'react-redux';

import './field.css';

const searchIcon = '../../assets/search/search.svg';

export const Field = ({ type, placeholder, onChange, id, value }) => {
    const { store } = useContext(ReactReduxContext);
    const [searchData, setSearchData] = useState([]);
    const navigate = useNavigate();

    const [noText, setNoText] = useState(true);

  
function HideAndShowPassword () {
    var x = document.getElementById(id);
    if (x.type === "password") {
        x.type = "text";
    } else {
        x.type = "password";
    }}

    const userOptions = {
        method: 'GET',
        headers:  { 'Content-Type': 'application/json', 'accept': 'application/json', 'authorization': `${store.getState().user.user_token}` },
    };
    function onSearchChange(event) {
        event.target.value === '' ? setNoText(true) : setNoText(false);
        fetch(`http://localhost:4000/tags/search/${event.target.value}?tables=masterclass&tables=biography&tables=partition&tables=work_analysis`, userOptions)
            .then((response) => response.json())
            .then(data => {
                setSearchData(data);
        })
        .catch((err) => {
            console.log('ERROR', err.message);
        })
        console.log(searchData);
    }

    return (
        <>
            <div className={['input-wrap', `input-wrap-${type}`].join(' ')}>
                <input
                    className={['field-input', `field-input-${type}`].join(' ')}
                    type={type}
                    placeholder={placeholder}
                    onChange={type === 'search' ? onSearchChange : onChange}
                    id={id}
                    defaultChecked={false}
                    value={value}
                />
                <svg  
                    className={['field-icon', `field-icon-${type}`].join(' ')}
                    onClick={HideAndShowPassword}/>
            </div>
            <div style={{display: 'flex', justifyContent: 'center'}}>
                <ul style={noText ? {display: 'none'} : null} className='results-block-searchable'>

                    <div>
                        <h2 className='title-search-category'>Masterclass</h2>
                        {searchData[0]?.length > 0 ? searchData[0].map((el) => {return (<li onClick={() => (navigate(`/Masterclass/${el.id}`))} className='li-custom font'>{el.title}</li>)}) : <div style={{textAlign: 'center', fontStyle: 'italic'}}>No results</div>}
                        <hr className='custom-search-hr' />
                    </div>

                    <div>
                        <h2 className='title-search-category'>Biography</h2>
                        {searchData[1]?.length > 0 ? searchData[1].map((el) => {return (<li className='li-custom font'>{el.first_name}</li>)}) : <div style={{textAlign: 'center', fontStyle: 'italic'}}>No results</div>}
                        <hr className='custom-search-hr' />
                    </div>

                    <div>
                        <h2 className='title-search-category'>Partition</h2>
                        {searchData[2]?.length > 0 ? searchData[2].map((el) => {return (<li className='li-custom font'></li>)}) : <div style={{textAlign: 'center', fontStyle: 'italic'}}>No results</div>}
                        <hr className='custom-search-hr' />
                    </div>

                    <div>
                        <h2 className='title-search-category'>Work Analysis</h2>
                        {searchData[3]?.length > 0 ? searchData[3].map((el) => {return (<li className='li-custom font'>{el.title}</li>)}) : <div style={{textAlign: 'center', fontStyle: 'italic'}}>No results</div>}
                        <hr className='custom-search-hr' />
                    </div>


                </ul>
            </div>
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