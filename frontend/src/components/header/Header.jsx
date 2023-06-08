import React from 'react';
import PropTypes from 'prop-types';
import Avatar from '../avatar/Avatar';
import Field from '../field/Field';

import './header.css';

export const Header = ({academyName}) => {
    return (
        <div className="header">
            <div className='header-group'>
                <div className="header-logo">
                    <Avatar />
                </div>
                <div className="header-title">
                    {academyName}
                </div>
            </div>
            <div className="header-searchbar">
                <Field type={"search"} placeholder={"Search for a professor, a composer, an instrument, a piece..."}/>
            </div>
            <div className='header-group'>
                <div className="header-create-dropdown">
                    <img src={"src/assets/header/create.svg"} />
                </div>
                <div className="header-user">
                    <Avatar/>
                </div>
            </div>
        </div>
    );
}
