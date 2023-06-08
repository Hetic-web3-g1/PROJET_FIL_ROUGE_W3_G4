import React from 'react'
import propTypes from 'prop-types'

import './uploadCard.css'
import Divider from '../divider/Divider'
import Button from '../button/Button'

export const UploadCard = ({  }) => {
    return (
        <div className="upload-card">
            <div className="upload-card-content">
                <div className="upload-card-drop">
                    Drop Here
                </div>
                <Divider text={"Or"}/>
                <div className='upload-card-upload-button'>
                    <input type='file' id='file'  hidden/>
                    <label for='file' className='upload-card-inputfile'>
                        Upload
                    </label>
                </div>
            </div>
        </div>
    );
}

export default UploadCard;
