import React from 'react';
import PropTypes from 'prop-types';
import './Login.css';
import Button from '../../components/button/Button';
import Field from '../../components/field/Field';

export const Login = ({ }) => {
  return (
    <div className="login-wrap">
      <img
        className='login-logo'
        srcset={`src/assets/Logo.svg`} >
      </img>
      <div className="login-form">
          <label for="email" className='login-field'>Email</label>
          <Field type="email" placeholder="Enter your mail" />
          <label for="password" className='login-field' >Password</label>
          <Field type="password" placeholder="Enter your password" />
          <Button label="Login" class="button button-secondary padded" />
      </div>
    </div>
  );
}; 
export default Login;