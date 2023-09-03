import React, {useContext, useState} from 'react';
import { ReactReduxContext } from 'react-redux'
import { useDispatch } from "react-redux";
import { ProfileActions } from '../../features/actions/profile';
import { useToast } from '../../utils/toast';

import './Profile.css';
import {Field} from '../../components/field/Field';
import {Header} from '../../components/header/Header';
import {Button} from '../../components/button/Button';
import { Dropdown } from '../../components/dropdown/Dropdown';

export const Profile = () => {

    const dispatch = useDispatch();
    const { store } = useContext(ReactReduxContext)
    const profile = store.getState().user.profile
    const toast = useToast();

    //Profile update states
    const [firstName, setFirstName] = useState(profile?.first_name)
    const [lastName, setLastName] = useState(profile?.last_name)
    const [email, setEmail] = useState(profile?.email)
    const isAdmin = profile?.primary_role == "admin" ? true : false;

    //Create user states
    const [user_firstName, setUserFirstName] = useState("")
    const [user_lastName, setUserLastName] = useState("")
    const [user_email, setUserEmail] = useState("")
    const [user_primaryRole, setUserPrimaryRole] = useState("user")

    const handleSaveProfile = (e) => {
        e.preventDefault();
        const userOptions = {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json', 'accept': 'application/json', 'authorization': `${store.getState().user.user_token}` },
            body: JSON.stringify({
                first_name: firstName,
                last_name: lastName,
                email: email,
                academy_id: profile.academy_id,
            }),
        }
        fetch(`http://${import.meta.env.VITE_API_ENDPOINT}/users/user/${profile.id}`, userOptions).then((response) => response.json()).then(data => {
            dispatch(ProfileActions.updateProfile({                
                first_name: firstName,
                last_name: lastName,
                email: email,
            }))
        });
    }

    const handleCreateUser = (e) => {
        e.preventDefault();
        const userOptions = {
            method: 'POST',
            headers: { 'Content-Type': 'application/json', 'accept': 'application/json', 'authorization': `${store.getState().user.user_token}` },
            body: JSON.stringify({
                first_name: user_firstName,
                last_name: user_lastName,
                email: user_email,
                academy_id: profile.academy_id,
                primary_role: user_primaryRole,
            }),
        }
        fetch(`http://${import.meta.env.VITE_API_ENDPOINT}/users/academy/${profile.academy_id}/user`, userOptions).then((response) => response.json()).then(data => {
            console.log(data)
        });
    }

    return (
        <div className="profile">
            <div className="profile-header">
                <Header/>
            </div>
            <form className="profile-wrap">
                <div className="profile-field">
                    First Name
                    <Field label="First name" type="text" placeholder="First name" value={`${firstName}`} onChange={(e) => setFirstName(e.target.value)}/>
                </div>
                <div className="profile-field">
                    Last Name
                    <Field label="Last name" type="text" placeholder="Last name" value={`${lastName}`} onChange={(e) => setLastName(e.target.value)}/>
                </div>
                <div className="profile-field">
                    Email
                    <Field label="Email" type="email" placeholder="Email" value={`${email}`} onChange={(e) => setEmail(e.target.value)}/>
                </div>
                <div className="profile-save">
                    <Button label="Save" onClick={(e) => {handleSaveProfile(e)}}/>
                </div>
            </form>
            {
                isAdmin ?
                <div className="profile-admin">
                    <div className="profile-admin-title">
                        Admin Panel
                    </div>
                    <form className="profile-wrap">
                        <div className="profile-field">
                            First Name
                            <Field label="First name" type="text" placeholder="First name" onChange={(e) => setUserFirstName(e.target.value)}/>
                        </div>
                        <div className="profile-field">
                            Last Name
                            <Field label="Last name" type="text" placeholder="Last name" onChange={(e) => setUserLastName(e.target.value)}/>
                        </div>
                        <div className="profile-field">
                            Email
                            <Field label="Email" type="email" placeholder="Email" onChange={(e) => setUserEmail(e.target.value)}/>
                        </div>
                        <div className="profile-field">
                            Role
                            <Dropdown callback={(e) => setUserPrimaryRole(e)} options={['user', 'admin']} defaultValue="user"/>
                        </div>
                        <div className="profile-user-create">
                            <Button label="Create User" onClick={(e) => {handleCreateUser(e)}}/>
                        </div>
                    </form>
                    <div className="profile-admin-title">
                        Toast Panel
                    </div>
                    <div className="profile-admin-toast-test">
                        <Button label="Test failure Toast" onClick={() => {toast.open({ type: 'failure', message: 'Failure test' })}}/>
                        <Button label="Test success Toast" onClick={() => {toast.open({ type: 'success', message: 'Success test' })}}/>
                        <Button label="Test warning Toast" onClick={() => {toast.open({ type: 'warning', message: 'Warning test' })}}/>
                    </div>
                </div>
                : null
            }
        </div>
    );
}

export default Profile;
