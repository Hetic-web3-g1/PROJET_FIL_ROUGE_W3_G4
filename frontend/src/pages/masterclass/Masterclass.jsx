import React, {useContext, useEffect} from "react";

import './Masterclass.css'

import { Header } from "../../components/header/Header";
import { Sidebar } from "../../components/sidebar/Sidebar";
import { MasterCard } from "../../components/masterCard/MasterCard";

import { useNavigate } from "react-router-dom";
import { ReactReduxContext } from 'react-redux'

import MasterCardData from '../../mocks/masterCardMocks'

export const Masterclass = () => {

    return (
        <div className="home">
          Work!
        </div>
    );
}

export default Masterclass;