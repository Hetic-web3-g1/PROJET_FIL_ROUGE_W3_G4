import React from 'react';
import './DashboardTeam.css';

import Select from 'react-select';

const DashboardTeam = (users) => {

    const roles = 
    {
        'Administrator' : 'Administrator can do everything',
        'Video Editor'  : 'Video Editor can do everything except delete users',
        'Writer'        : 'Writer can do everything except delete users',
        'Traductor'     : 'Traductor can do everything except delete users',
        'Professor'     : 'Professor can do everything except delete users',
    };

    var userList = [];

    for (var i = 0; i < users.users.length; i++) {
        userList.push({value: users.users[i].id, label: users.users[i].first_name + " " + users.users[i].last_name});
    }

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
                        <Select
                            closeMenuOnSelect={false}
                            isMulti
                            options={userList}
                        />
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
}

export default DashboardTeam;