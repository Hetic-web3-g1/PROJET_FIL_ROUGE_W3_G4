import React, {useState, useContext} from 'react';
import './resetPassword.css';
import Button from '../../../components/button/Button';
import Field from '../../../components/field/Field';
import { useNavigate } from "react-router-dom";

export const ResetPasswordEmail = ({ }) => {
  const [email, setEmail] = useState('');
  const navigate = useNavigate();

  const resetEmailForm = (e) => { 
      e.preventDefault();
      const emailOptions = {
        method: 'GET',
        headers: { 'Content-Type': 'application/json', 'accept': 'application/json' },
      };
      fetch(`http://${import.meta.env.VITE_API_ENDPOINT}/auth/forgot-password?email=${email}`, emailOptions).then((response) => response.json()).then(data => {
        if (data.detail != "Invalid Credentials") {
          navigate(`/reset-password/${data.token}`);
        } else {
          alert('Invalid Email');
        }
      });
  };

  return (
    <div className="reset-wrap">
      <form className="reset-form">
          <label for="password" className='reset-field'>Email</label>
          <Field type="email" placeholder="Enter your Email" onChange={(e) => {setEmail(e.target.value)}}/>
          <Button label="reset" className="button button-secondary padded" onClick={resetEmailForm}/>
      </form>
    </div>
  );
}; 

export default ResetPasswordEmail;