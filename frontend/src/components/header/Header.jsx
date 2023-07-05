import React, {useState} from 'react';
import PropTypes from 'prop-types';
import Avatar from '../avatar/Avatar';
import Field from '../field/Field';
import Divider from '../divider/Divider';
import { ModalMasterClass } from '../Modal/modalMasterclass/ModalMasterclass';

import './header.css';

export const Header = ({academyName}) => {
    const [createModal, setCreateModal] = useState(false);
    const [createMasterClassModal, setCreateMasterClassModal] = useState(false);
    const [createBiographyModal, setCreateBiographyModal] = useState(false);
    const [createWorkAnalysisModal, setCreateWorkAnalysisModal] = useState(false);

    const handleCreateModal = () => {
        setCreateModal(!createModal);
    }

    const handleCreateMasterClass = () => {
        setCreateMasterClassModal(!createMasterClassModal);
    }

    const handleCloseModalMasterClass = () => {
        setCreateMasterClassModal(!createMasterClassModal);
    }

    const handleCreateBiography = () => {
        setCreateBiographyModal(!createBiographyModal);
    }

    const handleCreateWorkAnalysis = () => {
        setCreateWorkAnalysisModal(!createWorkAnalysisModal);
    }

    return (
        <>
            {
                createMasterClassModal ? <ModalMasterClass handleClose={handleCloseModalMasterClass}/> : null
            }
            <div className="header">
                <div className='header-group'>
                    <div className="header-logo">
                        <Avatar />
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

                    <div className="header-user no-select">
                        <Avatar/>
                    </div>
                </div>
            </div>
        </>
    );
}
