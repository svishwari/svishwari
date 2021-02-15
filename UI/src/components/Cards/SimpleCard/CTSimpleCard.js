import React from 'react';
import Card from 'react-bootstrap/Card';
import './CTSimpleCard.scss';

const CTSimpleCard = ({cardComponent,onClickFn,width='100%',customClass='',children,...props}) => {
    return (
        <Card 
            onClick={onClickFn} 
            className={`ct-card-wrapper ${customClass}`}
            {...props}
            style={{width: width}}
        >
            {cardComponent}
            {children}
        </Card>
    )
}

export default CTSimpleCard
