import React, {useState, useContext, useEffect} from 'react';
import PropTypes from 'prop-types';
import './Login.css';
import Button from '../../../components/button/Button';
import Field from '../../../components/field/Field';
import { useDispatch } from "react-redux";
import { ProfileActions } from '../../../features/actions/profile';
import { useNavigate } from "react-router-dom";
import { ReactReduxContext } from 'react-redux'

export const Login = ({ }) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const { store } = useContext(ReactReduxContext)
      
  useEffect(() => {
    if(store.getState().user.user_token) {
      navigate("/home");
    }
  }, [store.getState().user.user_token])

  const loginForm = (e) => { 
    e.preventDefault();
    const loginOptions = {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'accept': 'application/json' },
      body: JSON.stringify({email, password }),
    };
    fetch(`http://${import.meta.env.VITE_API_ENDPOINT}/auth/login`, loginOptions).then((response) => response.json()).then(data => {
      if (data.detail != "Invalid Credentials") {
        dispatch(ProfileActions.login(data));
        navigate("/home");
      } else {
        alert('Invalid user');
      }
    });
  };

  return (
    <div className="login-wrap">
      <img
        className='login-logo'
        srcSet={`src/assets/Logo.svg`} >
      </img>
      <form className="login-form">
          <label for="email" className='login-field'>Email</label>
          <Field type="email" placeholder="Enter your mail" onChange={(e) => {setEmail(e.target.value)}}/>
          <label for="password" className='login-field' >Password</label>
          <Field type="password" placeholder="Enter your password" onChange={(e) => {setPassword(e.target.value)}}/>
          <Button label="Login" className="button button-secondary padded" onClick={loginForm}/>
      </form>
    </div>
  );
}; 
export default Login;