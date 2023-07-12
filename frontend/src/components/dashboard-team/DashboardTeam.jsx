import React from 'react'
import propTypes from 'prop-types'

import './dashboardteam.css'
import './../textstyle/textstyles.css'

import Field from '../field/Field.jsx'
import Roles from '../../mocks/roleMocks.js' 
import Dropdown from '../dropdown/Dropdown.jsx'
import Button from '../button/Button'


export const DashboardTeam = ({ MasterCardData, Videoname }) => {
    return ( 
        <div className='team-container'>
        <div className='team-header'>
            <span className='subtitle2'>Role</span>

            <div className='rect-container'>
            <div className='rect'></div>
            <span className='subtitle2'>Name</span>
            </div>
            <div className='rect-container'>
            <div className='rect'></div>
            <span className='subtitle2'>Description</span>
            </div>
            <Button label='Add New User'/>
        </div>

        {Roles.map((role, index) =>  {
            return (
                <div>
                    <div className='line'></div>

                <div key={index} className='role-list'>
                    <span className='subtitle2 roles'>{role.role}</span>
                    <div className='width-fix-1'>
                        <img className='role-avatar' src={role.avatar}></img>
                        <span className='subtitle2'>{role.name}</span>
                    </div>
                    <span className='width-fix-2 subtitle2'>{role.description}</span>
                    <div></div>
                </div>
                </div>
        )})}
        <div className='line'></div>
        <div className='role-add'>
        <div className='role-container'>
        <Dropdown options={['Administrator', 'Video Editor', 'Writer', 'Traductor', 'Professor']} defaultValue={'Role'}/>
        </div>
        <div className='role-container'>
        <Dropdown options={['Administrator', 'Video Editor', 'Writer', 'Traductor', 'Professor']} defaultValue={'Role'}/>
        </div>
        <div className='description-container'>
        <Field placeholder='Description'/>
        </div>
        <Button label='Add'/>
        </div>
        <div className='line'></div>

        </div>
    )}

    DashboardTeam.propTypes = {
        title: propTypes.string.isRequired,
        description: propTypes.string.isRequired,
    }

    DashboardTeam.defaultProps = {
        title: 'Upload Video',
        description: 'Upload your video here',
    }

    export default DashboardTeam;
        