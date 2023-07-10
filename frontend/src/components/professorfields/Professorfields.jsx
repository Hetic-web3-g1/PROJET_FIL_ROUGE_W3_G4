import React from 'react'
import Field from '../field/Field'

import './professorfields.css'

export const Professorfields = ({ }) => {

    return (
        <div>
        <div className='field-container'>
            <div className='modal-bio-prof-infos-field marg-right'>
                <span>Nationality</span>
                <Field placeholder="Nationality"/>
            </div>
            <div className='modal-bio-prof-infos-field fix-width'>
                <span>Website</span>
                <Field placeholder="Website"/>
            </div>
        </div>
        <div className='modal-bio-prof-infos-field full-width'>
            <span>Awards</span>
            <Field placeholder="Awards"/>
        </div>
        {/* <div className='modal-bio-prof-infos-field full-width-flex'>
            <img className='marg-right' src='src/assets/plus.svg'/> 
            <Field placeholder="Awards"/>
        </div> */}
    </div>
    )
}

export default Professorfields;
