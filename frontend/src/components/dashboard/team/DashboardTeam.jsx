import React from 'react';

import Dropdown from '../../dropdown/Dropdown';
import './DashboardTeam.css';

const DashboardTeam = (users) => {

    const roles = 
    {
        'Administrator' : 'Administrator can do everything',
        'Video Editor'  : 'Video Editor can do everything except delete users',
        'Writer'        : 'Writer can do everything except delete users',
        'Traductor'     : 'Traductor can do everything except delete users',
        'Professor'     : 'Professor can do everything except delete users',
    };

    return(
        <div className="dashboard-team">
            <div className="dashboard-team-header">
                <div>
                    Role
                </div>
                <div className="vl" />
                <div>
                    Description
                </div>
                <div className="vl" />
                <div>
                    Assigned User
                </div>
            </div>
            <div className="dashboard-team-body">
                {Object.keys(roles).map((role) => (
                    <div className="dashboard-team-body-row">
                        <div className="dashboard-team-role-name">
                            {role}
                        </div>
                        <div className="dashboard-team-role-description">
                            {roles[role]}
                        </div>
                        <div className="dashboard-team-role-user">
                            <Dropdown />
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
}

export default DashboardTeam;