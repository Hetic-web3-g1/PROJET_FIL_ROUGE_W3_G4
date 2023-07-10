import React, {useContext, useEffect} from "react";

import './home.css'

import { Header } from "../../components/header/Header";
import { Sidebar } from "../../components/sidebar/Sidebar";
import { MasterCard } from "../../components/masterCard/MasterCard";
import { useSelector } from 'react-redux';

import MasterCardData from '../../mocks/masterCardMocks'

export const Home = () => {
  const userStateRedux = useSelector((state) => state.filters.filters.sort_by);

  useEffect(() => {
    console.log('TEST', userStateRedux);
    switch (userStateRedux) {
        case 'Created at':
            console.log('created', MasterCardData);
            MasterCardData.sort((a, b) => {
                return new Date(b.created_at) - new Date(a.created_at);
            });
            break;

        case 'Last update':
            console.log('updated');
            break;
    }
  }, [userStateRedux]);
  
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