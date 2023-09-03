import React, {useState, useContext} from 'react';
import './resetPassword.css';
import Button from '../../../components/button/Button';
import Field from '../../../components/field/Field';
import { useNavigate } from "react-router-dom";
import { useToast } from '../../../utils/toast';

export const ResetPasswordEmail = ({ }) => {
  const [email, setEmail] = useState('');
  const navigate = useNavigate();
  const toast = useToast();

  const resetEmailForm = (e) => { 
      e.preventDefault();
      const emailOptions = {
        method: 'GET',
        headers: { 'Content-Type': 'application/json', 'accept': 'application/json' },
      };
      fetch(`http://${import.meta.env.VITE_API_ENDPOINT}/auth/forgot-password?email=${email}`, emailOptions).then((response) => response.json()).then(data => {
        if (data) {
          navigate(`/reset-password/${data.token}`);
        } else {
          toast.open({message: 'Invalid Email', type: 'failure'});
        }
      });
  };

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