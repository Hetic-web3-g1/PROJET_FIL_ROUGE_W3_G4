import React, {useState, useContext, useEffect} from 'react';
import './resetPassword.css';
import Button from '../../../components/button/Button';
import Field from '../../../components/field/Field';
import { useNavigate } from "react-router-dom";
import { useToast } from '../../../utils/toast';

import { resetPassword } from '../../../services/auth';

export const ResetPassword = ({ }) => {
  
  const navigate = useNavigate();
  const toast = useToast();

  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [passwordData, setPasswordData] = useState(null);
  const token = window.location.href.split('/')[4];

  const resetForm = (e) => { 
    e.preventDefault();
    resetPassword(token, password, confirmPassword, toast, setPasswordData);
  };

  useEffect(() => {
    if(passwordData) {
      navigate(`/login`);
    }
  }, [passwordData])

  return (
    <div className="reset-wrap">
      <form className="reset-form">
          <label htmlFor="password" className='reset-field'>Password</label>
          <Field type="password" placeholder="Enter your password" onChange={(e) => {setPassword(e.target.value)}}/>
          <label htmlFor="password" className='reset-field' >Confirm Password</label>
          <Field type="password" placeholder="Confirm your password" onChange={(e) => {setConfirmPassword(e.target.value)}}/>
          <Button label="reset" className="button button-secondary padded" onClick={resetForm}/>
      </form>
    </div>
  );
}; 

export default ResetPassword;