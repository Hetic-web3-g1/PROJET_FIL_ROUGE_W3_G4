import React, {useContext, useState} from 'react';
import { ReactReduxContext } from 'react-redux'
import { useDispatch } from "react-redux";

import './Profile.css';
import {Field} from '../../components/field/Field';
import {Header} from '../../components/header/Header';
import {Button} from '../../components/button/Button';

export const Profile = () => {

    const dispatch = useDispatch();
    const { store } = useContext(ReactReduxContext)
    const profile = store.getState().user.profile

    const [firstName, setFirstName] = useState(profile.first_name)
    const [lastName, setLastName] = useState(profile.last_name)
    const [email, setEmail] = useState(profile.email)

    const handleSave = () => {
        const userOptions = {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json', 'accept': 'application/json', 'authorization': `${store.getState().user.user_token}` },
            body: JSON.stringify({
                first_name: firstName,
                last_name: lastName,
                email: email,
            }),
        }
        fetch(`http://localhost:4000/users/user/${profile.id}`, userOptions).then((response) => response.json()).then(data => {
            dispatch(ProfileActions.updateProfile(profile = {                
                first_name: firstName,
                last_name: lastName,
                email: email,
            }))
        });
    }

    return (
        <div className="profile">
            <div className="profile-header">
                <Header academyName="Flamingo Academy"/>
            </div>
            <form className="profile-wrap">
                <div className="profile-field">
                    First Name
                    <Field label="First name" type="text" placeholder="First name" value={`${profile.first_name}`} onChange={(e) => setFirstName(e.target.value)}/>
                </div>
                <div className="profile-field">
                    Last Name
                    <Field label="Last name" type="text" placeholder="Last name" value={`${profile.last_name}`} onChange={(e) => setLastName(e.target.value)}/>
                </div>
                <div className="profile-field">
                    Email
                    <Field label="Email" type="email" placeholder="Email" value={`${profile.email}`} onChange={(e) => setEmail(e.target.value)}/>
                </div>
                <div className="profile-save">
                    <Button label="Save" type="primary" onClick={() => {handleSave()}}/>
                </div>
            </form>
        </div>
    );
}

export default Profile;
