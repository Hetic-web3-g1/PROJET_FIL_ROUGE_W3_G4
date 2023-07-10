import React, {useEffect, useState} from "react";

import './home.css'

import { Header } from "../../components/header/Header";
import { Sidebar } from "../../components/sidebar/Sidebar";
import { MasterCard } from "../../components/masterCard/MasterCard";
import { useSelector } from 'react-redux';

import MasterCardData from '../../mocks/masterCardMocks'

export const Home = () => {
  const userStateRedux = useSelector((state) => state.filters.filters.sort_by);
  const [mastercardComponent, setMastercardComponent] = useState([]);

  useEffect(() => {
    setMastercardComponent([]);
    switch (userStateRedux) {
        case 'Created at':
            const sortedDataByCreation = MasterCardData.sort((a, b) => {
                return new Date(b.created_at) - new Date(a.created_at);
            });
            sortedDataByCreation.map(e => setMastercardComponent(component => [...component, <MasterCard content={e} key={e.id}/>]));
            break;

        case 'Last update':
            const sortedDataByUpdate = MasterCardData.sort((a, b) => {
                return new Date(b.updated_at) - new Date(a.updated_at);
            });
            sortedDataByUpdate.map(e => setMastercardComponent(component => [...component, <MasterCard content={e} key={e.id}/>]));
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
                        mastercardComponent.map(mastercard => { return mastercard })
                    }
                </div>
            </div>
        </div>
    );
}

export default Home