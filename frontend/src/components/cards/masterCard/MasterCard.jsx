import React, {useState, useEffect, useMemo} from 'react';
import PropTypes from 'prop-types';

import { Label } from '../../label/Label'

import './MasterCard.css';

import placeholderImg from '../../../assets/cardPlaceholder.png';
import partitionPlaceholder from '../../../assets/partitionPlaceholder.png';

export const MasterCard = ({type, content, token, ...props }) => {

    const createdAt = new Date(content.created_at);
    const cardImg = type === 'masterCard' ? placeholderImg : partitionPlaceholder;

    const [createdBy, setCreatedBy] = useState('');

    useMemo(() => {
        const userOptions = {
            method: 'GET',
            headers:  { 'Content-Type': 'application/json', 'accept': 'application/json', 'authorization': `${token}` },
        };
        fetch(`http://localhost:4000/users/${content.created_by}`, userOptions).then((response) => response.json()).then(data => {
            setCreatedBy(data.first_name + ' ' + data.last_name);
        });
    },[])            

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
                            {createdBy}
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