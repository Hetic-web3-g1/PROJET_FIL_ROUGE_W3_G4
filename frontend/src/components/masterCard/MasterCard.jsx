import React from 'react';
import PropTypes from 'prop-types';

import { Label } from '../label/Label'

import './MasterCard.css';

export const MasterCard = ({type, content, ...props }) => {
    return (
        <div
            type="masterCard"
            className={['masterCard', `masterCard-${type}`].join(' ')}
            {...props}
        >
            <div className='masterCard-content'>
                <div className='masterCard-content-header'>
                    <div className='masterCard-content-title'>
                        {content.title}
                    </div>
                    <div className='masterCard-content-label'>
                        <Label type={content.status} label={content.status}/>
                    </div>
                </div>
                <div className='masterCard-content-description'>
                    <div>
                        {content.instrument}
                    </div>
                    <div>
                        {content.created_by}
                    </div>
                    <div>
                        {content.description}
                    </div>                  
                </div>
            </div>
        </div>
    );
}

export default MasterCard;