import React, {useContext} from 'react';
import { ReactReduxContext } from 'react-redux'
import './DashboardTeam.css';

import Select from 'react-select';

const DashboardTeam = ({ users, masterclassData }) => {

    const { store } = useContext(ReactReduxContext)
    const [userRoleList, setUserRoleList] = React.useState();
    const roles = 
    {
        'Administrator' : 'Administrator can do everything',
        'Video Editor'  : 'Video Editor can do everything except delete users',
        'Writer'        : 'Writer can do everything except delete users',
        'Traductor'     : 'Traductor can do everything except delete users',
        'Professor'     : 'Professor can do everything except delete users',
    };

    var userList = [];

    for (var i = 0; i < users?.length; i++) {
        userList.push({value: users[i].id, label: users[i].first_name + " " + users[i].last_name});
    }

    const setUserRole = (e, role) => {
        var tmpList = [];
        e.map((user) => {
            var tmp = {};
            tmp['user_id'] = user.value;
            tmp['masterclass_id'] = masterclassData.id;
            tmp['masterclass_role'] = role;
            tmpList.push(tmp);
        });
        setUserRoleList(tmpList);
    }

    const handleSave = (e) => {
        e.preventDefault();
        userRoleList.map((user) => {
            const userOptions = {
                method: 'POST',
                headers: { 'Content-Type': 'application/json', 'accept': 'application/json', 'authorization': `${store.getState().user.user_token}` },
                body: JSON.stringify({
                    user_id: user.user_id,
                    masterclass_id: user.masterclass_id,
                    masterclass_role: user.masterclass_role,
                }),
            };
            fetch(`http://${import.meta.env.VITE_API_ENDPOINT}/masterclasses/masterclass/assign_user`, userOptions).then((response) => response.json()).then(data => {
                console.log(data);
            })
        });
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
                            onChange={(e) => setUserRole(e, role)}
                        />
                        </div>
                    </div>
                ))}
            </div>
            <button className="dashboard-team-save button button-medium button-primary" onClick={(e) => handleSave(e)}>Save</button>
        </div>
    );
}

export default DashboardTeam;