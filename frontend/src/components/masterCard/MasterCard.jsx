import React from 'react';
import PropTypes from 'prop-types';

import { Label } from '../label/Label'

import './masterCard.css';

import placeholderImg from '../../assets/cardPlaceholder.png';
import partitionPlaceholder from '../../assets/partitionPlaceholder.png';

export const MasterCard = ({type, content, ...props }) => {

    const createdAt = new Date(content.created_at);
    const cardImg = type === 'masterCard' ? placeholderImg : partitionPlaceholder;
    console.log(cardImg)

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
                <div className='masterCard-content-details'>
                    <div>
                        {content.instrument}
                    </div>
                    <div className="masterCard-content-date-wrapper">
                        <div>
                            {content.created_by}
                        </div>
                        <div>
                            {createdAt.toLocaleDateString()}
                        </div>
                    </div>
                    <div className="masterCard-content-description">
                        {content.description}
                    </div>                  
                </div>
            </div>
            <div className="masterCard-img-wrapper">
                <img className='masterCard-img' src={cardImg} alt={content.title}/>
            </div>
        </div>
    );
}

MasterCard.propTypes = {
    type: PropTypes.oneOf(['masterCard', 'partition']),
    content: PropTypes.object.isRequired,
}

MasterCard.defaultProps = {
    type: 'masterCard',
};

export default MasterCard;