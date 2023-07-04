import React, {useContext, useEffect} from "react";

import './home.css'

import { Header } from "../../components/header/Header";
import { Sidebar } from "../../components/sidebar/Sidebar";

import { useNavigate } from "react-router-dom";
import { ReactReduxContext } from 'react-redux'

export const Home = () => {
    const navigate = useNavigate();
    const { store } = useContext(ReactReduxContext)
        
    useEffect(() => {
      if(!store.getState().user.user_token) {
        navigate("/");
      }
    }, [store.getState().user.user_token])

    return (
        <div className="home">
            <div className="home-header">
                <Header academyName="Flamingo Academy"/>
            </div>
            <div className="home-body">
                <Sidebar/>
            </div>
        </div>
    );
}

export default Home