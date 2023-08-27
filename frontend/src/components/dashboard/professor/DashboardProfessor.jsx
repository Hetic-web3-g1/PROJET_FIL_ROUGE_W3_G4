import React, {useState, useContext} from 'react'
import { ReactReduxContext } from 'react-redux'

import './DashboardProfessor.css'

import Field from '../../field/Field'

export const DashboardProfessor = ({masterclassData, handleSave}) => {

    const { store } = useContext(ReactReduxContext)

    const [searchProfessorData, setSearchProfessorData] = useState([])
    const [masterclass, setMasterclass] = useState([])

    const setProfessor = (id) => {
        var newMasterclassData = masterclassData
        newMasterclassData.teacher_bio_id = id
        setMasterclass(newMasterclassData)
    }

    const handleSearch = (e) => {
        const Options = {
            method: 'GET',
            headers:  { 'Content-Type': 'application/json', 'accept': 'application/json', 'authorization': `${store.getState().user.user_token}`},
          };
          fetch(`http://${import.meta.env.VITE_API_ENDPOINT}/tags/search/${e.target.value}?tables=biography`, Options).then((response) => response.json()).then(data => {
            setSearchProfessorData(data)
          });
    }

    return (
        <div className='professor'>
            <div className="professor-searchbar">
                <Field type={"search"} placeholder={"Search for a professor"} onChange={e => handleSearch(e)}/>
            </div>
            <ul className="professor-list">
                {searchProfessorData[0]?.map((professor) => {
                    return (
                        <li className="li-custom font" onClick={() => (setProfessor(professor.id))}>
                            {professor.first_name} {professor.last_name}
                        </li>
                    )
                })}
            </ul>
            <button onClick={e => handleSave(e, masterclass)}>Save</button>
        </div>
    );
};

export default DashboardProfessor;