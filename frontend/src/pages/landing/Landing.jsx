import React, {useContext, useEffect} from 'react';
import PropTypes from 'prop-types';
import './Landing.css';
import Button from '../../components/button/Button';
import { Link } from "react-router-dom";
import { ReactReduxContext } from 'react-redux'
import { useNavigate } from "react-router-dom";

export const Landing = ({ }) => {
  const navigate = useNavigate();
  const { store } = useContext(ReactReduxContext)
      
  useEffect(() => {
    if(store.getState().user.user_token) {
      navigate("/home");
    }
  }, [store.getState().user.user_token])

  return (
    <div className="landing-wrap">
      <img
        className='landing-logo'
        srcSet={`../src/assets/Logo.svg`} >
      </img>
      <Link to="/login">
        <Button label="Enter" className="button button-primary padded"/>
      </Link>
    </div>
  );
};

export default Landing;