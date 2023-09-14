import React, {useState, useContext, useEffect} from 'react';
import PropTypes from 'prop-types';
import './Login.css';
import Button from '../../../components/button/Button';
import Field from '../../../components/field/Field';
import { useDispatch } from "react-redux";
import { ProfileActions } from '../../../features/actions/profile';
import { useNavigate } from "react-router-dom";
import { ReactReduxContext } from 'react-redux'
import { Link } from "react-router-dom";
import { useToast } from '../../../utils/toast';

import { login } from '../../../services/auth';

export const Login = ({ }) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loginData, setLoginData] = useState(null);
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const { store } = useContext(ReactReduxContext)
  const toast = useToast();
      
  useEffect(() => {
    if(store.getState().user.user_token) {
      navigate("/home");
    }
  }, [store.getState().user.user_token])

  useEffect(() => {
    if(loginData) {
      dispatch(ProfileActions.login(loginData));
      navigate("/home");
    }
  }, [loginData])

  const handleLogin = (e) => { 
    e.preventDefault();
    login(email, password, setLoginData, toast);
  };

  return (
    <div className="login-wrap">
      <img
        className='login-logo'
        srcSet={`../src/assets/Logo.svg`} >
      </img>
      <form className="login-form">
          <label htmlFor="email" className='login-field'>Email</label>
          <Field type="email" placeholder="Enter your mail" onChange={(e) => {setEmail(e.target.value)}}/>
          <label htmlFor="password" className='login-field' >Password</label>
          <Field type="password" placeholder="Enter your password" onChange={(e) => {setPassword(e.target.value)}}/>
          <Button label="Login" className="button button-secondary padded" onClick={handleLogin}/>
          <div className='reset-password-link'>Forgot your password ? <Link to="/reset-password">Reset Password</Link></div>
      </form>
    </div>
  );
}; 
export default Login;