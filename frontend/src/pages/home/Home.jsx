import React, {useEffect, useState, useContext} from "react";

import './home.css'

import { Header } from "../../components/header/Header";
import { Sidebar } from "../../components/sidebar/Sidebar";
import { MasterCard } from "../../components/cards/masterCard/MasterCard";
import { BiographyCard } from "../../components/cards/biographyCard/BIographyCard";
import { Spinner } from "../../components/spinner/Spinner";

import { useSelector, ReactReduxContext } from 'react-redux';

import MasterCardData from '../../mocks/masterCardMocks'
import { useNavigate } from "react-router-dom";
import { useTranslation } from 'react-i18next';

export const Home = () => {

    const userStateRedux = useSelector((state) => state.filters.filters.sort_by);
    const navigate = useNavigate();
    const { t, i18n } = useTranslation();

    const sortByState = useSelector((state) => state.filters.filters.sort_by);
    const sortByStatusState = useSelector((state) => state.filters.filters.sort_by_status);
    const [mastercardComponent, setMastercardComponent] = useState([]);
    const [mastercardData, setMastercardData] = useState([]);
    const [biographyData, setBiographyData] = useState();


    const [sortedTest, setSortedTest] = useState([]);

    const { store } = useContext(ReactReduxContext)

    const sortDataByLabel = () => {
        var activeFilters = [];
        sortByStatusState.map(e => {
            e[1] === true ? activeFilters.push(e[0]) : undefined;
        })

        var sortedArray = [];
        activeFilters.map(filter => {
            var mscCopy = mastercardData;
            sortedArray.push(mscCopy.filter(e => e.status === filter.toLowerCase()));
        })
        return sortedArray.flat();
    }

    const sortData = () => {
        const machin = sortDataByLabel();
        setMastercardComponent([]);
        switch (sortByState) 
            {
                case 'Created at':
                    const sortedDataByCreation = machin?.sort((a, b) => {
                        return new Date(b.created_at) - new Date(a.created_at);
                    });
                    sortedDataByCreation?.map(e => setMastercardComponent(component => [...component, <MasterCard content={e} key={e.id} token={store.getState().user.user_token} onClick={() => (navigate(`/Masterclass/${e.id}`))}/>]));
                    break;

                case 'Last update':
                    const sortedDataByUpdate = machin?.sort((a, b) => {
                        return new Date(b.updated_at) - new Date(a.updated_at);
                    });
                    sortedDataByUpdate?.map(e => setMastercardComponent(component => [...component, <MasterCard content={e} key={e.id} token={store.getState().user.user_token} onClick={() => (navigate(`/Masterclass/${e.id}`))}/>]));
                    break;
            }
    }

    useEffect(() => {
        if(store.getState().user.user_token) {
            const userOptions = {
                method: 'GET',
                headers:  { 'Content-Type': 'application/json', 'accept': 'application/json', 'authorization': `${store.getState().user.user_token}` },
            };
            fetch(`http://${import.meta.env.VITE_API_ENDPOINT}/masterclasses`, userOptions).then((response) => response.json()).then(data => {
                setMastercardData(data)
            });
        }
    },[])

    useEffect(() => {
        if(store.getState().user.user_token) {
            const userOptions = {
                method: 'GET',
                headers:  { 'Content-Type': 'application/json', 'accept': 'application/json', 'authorization': `${store.getState().user.user_token}` },
            };
            fetch(`http://${import.meta.env.VITE_API_ENDPOINT}/biographies`, userOptions).then((response) => response.json()).then(data => {
                setBiographyData(data)
            });
        }
    },[])

    useEffect(() => {
        sortData();
    }, [sortByState, sortByStatusState]);
  
    return (
        <div className="home">
            <div className="home-header">
                <Header/>
            </div>
            <div className="home-body">
                <div className="home-sidebar">
                    <Sidebar categories={{Status: ['Completed', 'Created', 'In-review', 'In-progress', 'Archived']}}/>
                </div>
                {
                mastercardData ? 
                    <div className="home-content">
                        {
                            mastercardComponent.map(mastercard => { return mastercard })
                        }
                        {
                            biographyData?.map((bio, index) => {
                                return(
                                    <BiographyCard content={bio} key={`biography-${index}`}></BiographyCard>
                                )
                            })
                        }
                    </div>
                : 
                <div className="home-spin-wrap">
                    <Spinner />
                </div>
                } 
            </div>
        </div>
    );
}

export default Home