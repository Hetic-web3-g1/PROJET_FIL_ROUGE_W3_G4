import React, {useState, useEffect, useMemo} from 'react';
import PropTypes from 'prop-types';

import './biographyCard.css'

import awardIcon from '../../../assets/award/gg_awards.svg'
import partitionPlaceholder from '../../../assets/partitionPlaceholder.png';

export const BiographyCard = (biography) => {
    return(
        <div className='biographyCard'>
            <div className='biographyCard-content'>
                <div className='biographyCard-content-header'>
                    <div className='biographyCard-content-title'>
                        {biography.content.first_name + ' ' + biography.content.last_name}
                    </div>
                </div>
                <div className='biographyCard-content-details'>
                    <div>
                        {biography.content.instrument}
                    </div>
                    {biography.content.awards?.map((award, index) => {
                        return(
                            <div key={`biography-award-${index}`}>
                                {awardIcon}
                                {award}
                            </div>
                        )
                    })}
                    <div className="biographyCard-content-description">
                        {biography.content.content}
                    </div>                  
                </div>
            </div>
            <div className="biographyCard-img-wrapper">
                <img className='biographyCard-img' src={partitionPlaceholder} alt={biography.content.title}/>
            </div>
        </div>
    )
}

BiographyCard.propTypes = {
    content: PropTypes.object.isRequired
}

export default BiographyCard