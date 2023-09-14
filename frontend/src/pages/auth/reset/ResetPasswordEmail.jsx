import React, {useState, useContext, useEffect} from 'react';
import './resetPassword.css';
import Button from '../../../components/button/Button';
import Field from '../../../components/field/Field';
import { useNavigate } from "react-router-dom";
import { useToast } from '../../../utils/toast';

import { resetPasswordEmail } from '../../../services/auth';

export const ResetPasswordEmail = ({ }) => {
  const [email, setEmail] = useState('');
  const [resetData, setResetData] = useState(null);
  const navigate = useNavigate();
  const toast = useToast();

  const resetEmailForm = (e) => { 
    e.preventDefault();
    resetPasswordEmail(email, toast, setResetData);
  };

  useEffect(() => {
    if(resetData) {
      navigate(`/reset-password/${resetData.token}`);
    }
  }, [resetData])


  return (
    <div className="reset-wrap">
      <form className="reset-form">
          <label htmlFor="password" className='reset-field'>Email</label>
          <Field type="email" placeholder="Enter your Email" onChange={(e) => {setEmail(e.target.value)}}/>
          <Button label="reset" className="button button-secondary padded" onClick={resetEmailForm}/>
      </form>
    </div>
  );
}; 

export default ResetPasswordEmail;