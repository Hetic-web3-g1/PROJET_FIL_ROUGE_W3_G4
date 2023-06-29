import React, {useState} from 'react';
import PropTypes from 'prop-types';
import './Login.css';
import Button from '../../components/button/Button';
import Field from '../../components/field/Field';
import { getStore } from '../../utils';
import { ProfileActions } from '../../features/actions/profile';

export const Login = ({ }) => {
  const [userName, setUserName] = useState('');
  const [password, setPassword] = useState('');

  const loginForm = (e) => { 
    e.preventDefault();
    const user = getStore('user');
    if (user) {
      dispatch(ProfileActions.login(user));
      history.push('/dashboard');
    } else {
      alert('Invalid user');
    }
  };

  return (
    <div className="login-wrap">
      <img
        className='login-logo'
        srcSet={`src/assets/Logo.svg`} >
      </img>
      <form className="login-form">
          <label for="email" className='login-field'>Email</label>
          <Field type="email" placeholder="Enter your mail" onChange={(e) => {setUserName(e.target.value)}}/>
          <label for="password" className='login-field' >Password</label>
          <Field type="password" placeholder="Enter your password" onChange={(e) => {setPassword(e.target.value)}}/>
          <Button label="Login" className="button button-secondary padded" onClick={loginForm}/>
      </form>
    </div>
  );
}; 
export default Login;