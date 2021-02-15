import React from 'react';
import './CTCardGroup.scss';

const CardWrapper = ({children, ...props}) => {
    return (
        <div className='ct-card-group-wrapper' {...props}>
            {children}
        </div>
    )
}

export default CardWrapper
