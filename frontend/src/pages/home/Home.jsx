import React, {useContext, useEffect} from "react";

import './home.css'

import { Header } from "../../components/header/Header";
import { Sidebar } from "../../components/sidebar/Sidebar";
import { MasterCard } from "../../components/masterCard/MasterCard";

import MasterCardData from '../../mocks/masterCardMocks'

export const Home = () => {
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
                            return <MasterCard content={data} key={data.id}/>
                        }
                    )}
                </div>
            </div>
        </div>
    );
}

export default Home