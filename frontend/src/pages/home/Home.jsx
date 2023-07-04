import React, {useContext, useEffect} from "react";

import './home.css'

import { Header } from "../../components/header/Header";
import { Sidebar } from "../../components/sidebar/Sidebar";
import { MasterCard } from "../../components/masterCard/MasterCard";

import { useNavigate } from "react-router-dom";
import { ReactReduxContext } from 'react-redux'

import MasterCardData from '../../mocks/masterCardMocks'

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
                <div className="home-sidebar">
                    <Sidebar/>
                </div>
                <div className="home-content">
                    {
                        MasterCardData.map(function(data, index){
                            return <MasterCard content={data}/>
                        }
                    )}
                </div>
            </div>
        </div>
    );
}

export default Home