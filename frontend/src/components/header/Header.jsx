import React, {useState, useContext, useEffect} from 'react';

import Avatar from '../avatar/Avatar';
import Field from '../field/Field';
import Divider from '../divider/Divider';
import { ModalMasterClass } from '../Modal/modalMasterclass/ModalMasterclass';
import { ModalBioProf } from '../Modal/modalbioprof/ModalBioProf.jsx';
import { ModalWorkAnalysis } from '../Modal/modalworkanalysis/ModalWorkanalysis';
import { ReactReduxContext } from 'react-redux'
import { ProfileActions } from '../../features/actions/profile';
import { AcademyActions } from '../../features/actions/academy';
import { useDispatch } from "react-redux";
import { useNavigate } from "react-router-dom";
import { Link } from "react-router-dom";
import OutsideAlerter from '../../utils/clickOutside';

import { getUserAvatar, setLocaleUserData } from '../../services/user';
import { setLocaleAcademyData } from '../../services/academy';

import './Header.css';

export const Header = () => {

    const { store } = useContext(ReactReduxContext)
    const profile = store.getState().user.profile

    const [createModal, setCreateModal] = useState(false);
    const [createMasterClassModal, setCreateMasterClassModal] = useState(false);
    const [createBiographyModal, setCreateBiographyModal] = useState(false);
    const [createWorkAnalysisModal, setCreateWorkAnalysisModal] = useState(false);
    const [userModal, setUserModal] = useState(false);
    const [avatar, setAvatar] = useState(null);
    const dispatch = useDispatch();
    const navigate = useNavigate();

    useEffect(() => {
        if(!store.getState().user.user_token) {
          navigate("/");
        }
    }, [store.getState().user.user_token])
    
    useEffect(() => {
        if(store.getState().user.user_token) {
            if(!store.getState().user.profile?.id) {
                setLocaleUserData(store.getState().user.user_token, dispatch, ProfileActions)
            }
        }
    },)

    useEffect(() => {
        if(!store.getState().academy.academy?.id) {
            setLocaleAcademyData(store.getState().user.user_token, dispatch, store.getState().user.profile.academy_id, AcademyActions)
        }
    },)

    useEffect(() => {        
        if(store.getState().user?.image_id) {
            if(!avatar) {
                getUserAvatar(store.getState().user.user_token, profile, setAvatar)
            }
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
        navigate("/");
    }

    function handleDisplay(target) {
        target === 'modal' ? setCreateModal(false) : setUserModal(false);
    }

    return (
        <div id={"header"}>
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
                            <Avatar/>
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
                        <img src={"../src/assets/header/create.svg"} className={'pointer'} />
                        {
                            createModal ?
                                <OutsideAlerter returnValues={() => handleDisplay('modal')}>
                                    <div className="header-create-dropdown-content">
                                        <div className="header-create-dropdown-item">
                                            Masterclass
                                            <img className={'pointer'} src={"../src/assets/header/circle-plus.svg"}  onClick={() => handleCreateMasterClass()}/>
                                        </div>
                                        <Divider />
                                        <div className="header-create-dropdown-item">
                                            Biography
                                            <img className={'pointer'} src={"../src/assets/header/circle-plus.svg"} onClick={() => handleCreateBiography()}/>
                                        </div>
                                        <Divider />
                                        <div className="header-create-dropdown-item">
                                            Work Analysis
                                            <img className={'pointer'} src={"../src/assets/header/circle-plus.svg"} style={{marginLeft: "5px"}} onClick={() => handleCreateWorkAnalysis()}/>
                                        </div>
                                    </div>
                                </OutsideAlerter>
                            : 
                                null                         
                        }
                        
                    </div>

                    <div className="header-user no-select" onClick={() => setUserModal(!userModal)}>
                        <Avatar path={avatar?.url}/>
                        {
                            userModal ?
                                <OutsideAlerter returnValues={() => handleDisplay('user')}>
                                    <div className="header-create-dropdown-content">
                                        <div className="header-create-dropdown-item" onClick={() => navigate("/profile")}>
                                            Signed in as {profile?.first_name} {profile?.last_name}
                                        </div>
                                        <Divider />
                                        <div className="header-create-dropdown-item pointer hover" onClick={() => navigate("/profile")}>
                                            Profile
                                        </div>
                                        <div className="header-create-dropdown-item pointer hover" onClick={() => handleDisconnect()}>
                                            Disconnect
                                        </div>
                                    </div>
                                </OutsideAlerter>
                            :
                                null
                        }
                    </div>
                </div>
            </div>
        </div>
    );
}
