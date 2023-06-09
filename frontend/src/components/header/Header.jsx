import React, {useState, useContext, useEffect} from 'react';

import Avatar from '../avatar/Avatar';
import Field from '../field/Field';
import Divider from '../divider/Divider';
import { ModalMasterClass } from '../Modal/modalMasterclass/ModalMasterclass';
import { ModalBioProf } from '../Modal/modalbioprof/Modalbioprof.jsx';
import { ModalWorkAnalysis } from '../Modal/modalworkanalysis/ModalWorkanalysis';
import { ReactReduxContext } from 'react-redux'
import { ProfileActions } from '../../features/actions/profile';
import { AcademyActions } from '../../features/actions/academy';
import { useDispatch } from "react-redux";
import { useNavigate } from "react-router-dom";
import { Link } from "react-router-dom";

import './header.css';

export const Header = () => {
    const [createModal, setCreateModal] = useState(false);
    const [createMasterClassModal, setCreateMasterClassModal] = useState(false);
    const [createBiographyModal, setCreateBiographyModal] = useState(false);
    const [createWorkAnalysisModal, setCreateWorkAnalysisModal] = useState(false);
    const [userModal, setUserModal] = useState(false);
    const dispatch = useDispatch();
    const navigate = useNavigate();

    const { store } = useContext(ReactReduxContext)

    useEffect(() => {
        if(!store.getState().user.user_token) {
          navigate("/");
        }
      }, [store.getState().user.user_token])
    
    useEffect(() => {
        if(!store.getState().user.profile?.id) {
            const userOptions = {
                method: 'GET',
                headers:  { 'Content-Type': 'application/json', 'accept': 'application/json', 'authorization': `${store.getState().user.user_token}` },
            };
            fetch(`http://localhost:4000/users/user/me`, userOptions).then((response) => response.json()).then(data => {
                dispatch(ProfileActions.updateProfile(data));
            });
        }
    },)

    useEffect(() => {
        if(!store.getState().academy.academy?.id) {
            const userOptions = {
                method: 'GET',
                headers:  { 'Content-Type': 'application/json', 'accept': 'application/json', 'authorization': `${store.getState().user.user_token}` },
            };
            fetch(`http://localhost:4000/academies/${store.getState().user.profile.academy_id}`, userOptions).then((response) => response.json()).then(data => {
                dispatch(AcademyActions.setAcademy(data));
            });
        }
    },)

    const handleCreateModal = () => {
        setCreateModal(!createModal);
    }

    const handleCreateMasterClass = () => {
        setCreateMasterClassModal(!createMasterClassModal);
    }

    const handleCreateBiography = () => {
        setCreateBiographyModal(!createBiographyModal);
    }

    const handleCreateWorkAnalysis = () => {
        setCreateWorkAnalysisModal(!createWorkAnalysisModal);
    }

    const handleDisconnect = () => {
        dispatch(ProfileActions.disconnect());
        window.location.reload();
    }

    return (
        <>
            {
                createMasterClassModal ? <ModalMasterClass handleClose={handleCreateMasterClass} store={store}/> : null
            }
            {
                createBiographyModal ? <ModalBioProf handleClose={handleCreateBiography} store={store}/> : null
            }
            {
                createWorkAnalysisModal ? <ModalWorkAnalysis handleClose={handleCreateWorkAnalysis}/> : null
            }
            <div className="header">
                <div className='header-group'>
                    <div className="header-logo">
                        <Link to="/home">
                            <Avatar />
                        </Link>
                    </div>
                    <div className="header-title">
                        {store.getState().academy.academy.name}
                    </div>
                </div>
                <div className="header-searchbar">
                    <Field type={"search"} placeholder={"Search for a professor, a composer, an instrument, a piece..."}/>
                </div>
                <div className='header-group'>
                    <div className="header-create-dropdown" onClick={() => handleCreateModal()}>
                        <img src={"../src/assets/header/create.svg"} />
                        {
                            createModal ?
                                <>
                                    <div className="header-create-dropdown-content">
                                        <div className="header-create-dropdown-item">
                                            Masterclass
                                            <img src={"../src/assets/header/circle-plus.svg"}  onClick={() => handleCreateMasterClass()}/>
                                        </div>
                                        <Divider />
                                        <div className="header-create-dropdown-item">
                                            Biography
                                            <img src={"../src/assets/header/circle-plus.svg"} onClick={() => handleCreateBiography()}/>
                                        </div>
                                        <Divider />
                                        <div className="header-create-dropdown-item">
                                            Work Analysis
                                            <img src={"../src/assets/header/circle-plus.svg"} style={{marginLeft: "5px"}} onClick={() => handleCreateWorkAnalysis()}/>
                                        </div>
                                    </div>
                                </>
                            : 
                                null                         
                        }
                        
                    </div>

                    <div className="header-user no-select" onClick={() => setUserModal(!userModal)}>
                        <Avatar/>
                        {
                            userModal ?
                                <>
                                    <div className="header-create-dropdown-content">
                                        <div className="header-create-dropdown-item" onClick={() => navigate("/profile")}>
                                            Profile
                                        </div>
                                        <Divider />
                                        <div className="header-create-dropdown-item" onClick={() => handleDisconnect()}>
                                            Disconnect
                                        </div>
                                    </div>
                                </>
                            :
                                null
                        }
                    </div>
                </div>
            </div>
        </>
    );
}
