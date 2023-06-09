import React from "react";

import './home.css'

import { Header } from "../../components/header/Header";

export const Home = () => {
    return (
        <div className="home">
            <div className="home-header">
                <Header academyName="Flamingo Academy"/>
            </div>
        </div>
    );
}

export default Home