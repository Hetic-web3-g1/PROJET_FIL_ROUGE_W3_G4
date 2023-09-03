import React from 'react'
import PropTypes from 'prop-types'

import './Divider.css'

export const Divider = ({text}) => {
    return (
        text ? <div className='divider'>{text}</div> : <div className='divider-no-text'/>
    )
}

Divider.propTypes = {
    text: PropTypes.string
}

export default Divider;