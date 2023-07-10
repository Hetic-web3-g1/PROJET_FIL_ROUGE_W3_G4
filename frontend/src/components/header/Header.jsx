import React, {useState, useContext, useEffect} from 'react';

import Avatar from '../avatar/Avatar';
import Field from '../field/Field';
import Divider from '../divider/Divider';
import { ModalMasterClass } from '../Modal/modalMasterclass/ModalMasterclass';
import { ModalBioProf } from '../Modal/modalbioprof/Modalbioprof.jsx';
import { ModalWorkAnalysis } from '../Modal/modalworkanalysis/ModalWorkanalysis';
import { ReactReduxContext } from 'react-redux'
import { purgeStoredState } from 'redux-persist'
import { ProfileActions } from '../../features/actions/profile';
import { useDispatch } from "react-redux";
import { useNavigate } from "react-router-dom";
import { Link } from "react-router-dom";

import './header.css';

export const Header = ({academyName}) => {
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
        if(!store.getState().user.profile.id) {
            const userOptions = {
                method: 'GET',
                headers:  { 'Content-Type': 'application/json', 'accept': 'application/json', 'authorization': `${store.getState().user.user_token}` },
            };
            fetch(`http://localhost:4000/users/user/me`, userOptions).then((response) => response.json()).then(data => {
                dispatch(ProfileActions.updateProfile(data));
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
                createMasterClassModal ? <ModalMasterClass handleClose={handleCreateMasterClass}/> : null
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
                        {academyName}
                    </div>
                </div>
                <div className="header-searchbar">
                    <Field type={"search"} placeholder={"Search for a professor, a composer, an instrument, a piece..."}/>
                </div>
                <div className='header-group'>
                    <div className="header-create-dropdown" onClick={() => handleCreateModal()}>
                        <img src={"src/assets/header/create.svg"} />
                        {
                            createModal ?
                                <>
                                    <div className="header-create-dropdown-content">
                                        <div className="header-create-dropdown-item">
                                            Masterclass
                                            <img src={"src/assets/header/circle-plus.svg"} onClick={() => handleCreateMasterClass()}/>
                                        </div>
                                        <Divider />
                                        <div className="header-create-dropdown-item">
                                            Biography
                                            <img src={"src/assets/header/circle-plus.svg"} onClick={() => handleCreateBiography()}/>
                                        </div>
                                        <Divider />
                                        <div className="header-create-dropdown-item">
                                            Work Analysis
                                            <img src={"src/assets/header/circle-plus.svg"} onClick={() => handleCreateWorkAnalysis()}/>
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
                                    <div className="header-user-dropdown">
                                        <div className="header-user-dropdown-item" onClick={() => handleDisconnect()}>
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
