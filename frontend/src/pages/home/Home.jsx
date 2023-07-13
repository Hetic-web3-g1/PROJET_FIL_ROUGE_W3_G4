import React, {useEffect, useState, useContext} from "react";

import './home.css'

import { Header } from "../../components/header/Header";
import { Sidebar } from "../../components/sidebar/Sidebar";
import { MasterCard } from "../../components/masterCard/MasterCard";
import { useSelector, ReactReduxContext } from 'react-redux';

import MasterCardData from '../../mocks/masterCardMocks'
import { useNavigate } from "react-router-dom";

export const Home = () => {

    const userStateRedux = useSelector((state) => state.filters.filters.sort_by);
    const [mastercardComponent, setMastercardComponent] = useState([]);
    const [mastercardData, setMastercardData] = useState();
    const navigate = useNavigate();

    const { store } = useContext(ReactReduxContext)

    const sortData = () => {
        setMastercardComponent([]);
        switch (userStateRedux) {
            case 'Created at':
                const sortedDataByCreation = mastercardData?.sort((a, b) => {
                    return new Date(b.created_at) - new Date(a.created_at);
                });
                sortedDataByCreation?.map(e => setMastercardComponent(component => [...component, <MasterCard content={e} key={e.id} token={store.getState().user.user_token} onClick={() => (navigate(`/Masterclass/${e.id}`))}/>]));
                break;

            case 'Last update':
                const sortedDataByUpdate = mastercardData?.sort((a, b) => {
                    return new Date(b.updated_at) - new Date(a.updated_at);
                });
                sortedDataByUpdate?.map(e => setMastercardComponent(component => [...component, <MasterCard content={e} key={e.id} token={store.getState().user.user_token} onClick={() => (navigate(`/Masterclass/${e.id}`))}/>]));
                break;
        }
    }

    useEffect(() => {
            const userOptions = {
                method: 'GET',
                headers:  { 'Content-Type': 'application/json', 'accept': 'application/json', 'authorization': `${store.getState().user.user_token}` },
            };
            fetch(`http://localhost:4000/masterclasses`, userOptions).then((response) => response.json()).then(data => {
                setMastercardData(data)
            });
        },[])

    useEffect(() => {
        sortData();
    }, [userStateRedux ,mastercardData]);
  
    return (
        <div className="home">
            <div className="home-header">
                <Header/>
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