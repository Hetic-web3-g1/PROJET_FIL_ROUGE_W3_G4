import React, {useState, useContext} from 'react';
import './resetPassword.css';
import Button from '../../../components/button/Button';
import Field from '../../../components/field/Field';
import { useNavigate } from "react-router-dom";

export const ResetPassword = ({ }) => {
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const navigate = useNavigate();

  const token = window.location.href.split('/')[4];

  const resetForm = (e) => { 
    if (password != confirmPassword) {
      alert('Passwords do not match');
      return;
    }
    else {
      e.preventDefault();
      const resetOptions = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'accept': 'application/json' },
        body: JSON.stringify({password, token }),
      };
      fetch(`http://${import.meta.env.VITE_API_ENDPOINT}/auth/reset-password`, resetOptions).then((response) => response.json()).then(data => {
        if (data?.detail != "Invalid Credentials" && data?.detail != "Expired Token") {
          navigate("/login");
        } else {
          alert('Invalid Token');
        }
      });
    }
  };

  return (
    <div className="reset-wrap">
      <form className="reset-form">
          <label for="password" className='reset-field'>Password</label>
          <Field type="password" placeholder="Enter your password" onChange={(e) => {setPassword(e.target.value)}}/>
          <label for="password" className='reset-field' >Confirm Password</label>
          <Field type="password" placeholder="Confirm your password" onChange={(e) => {setConfirmPassword(e.target.value)}}/>
          <Button label="reset" className="button button-secondary padded" onClick={resetForm}/>
      </form>
    </div>
  );
}; 

export default ResetPassword;