import React from 'react';
import './CTImageCard.scss';
import Card from 'react-bootstrap/Card';

// There is a limitation here that cardImage size id fixed to 80px by 80px for now.
// In case of svg as a react component the color also needs to be applied within the svg component passed
// For other cases we can pass the color in imageColor prop

const CTImageCard = ({maxWidth=320,imageColor, cardImage,cardTitle='Title',cardDescription='',customClass='',children,...props}) => {
    return (
        <Card
            className={`ct-imagecard-wrapper ${customClass}`}
            {...props}
            style={{
                maxWidth: maxWidth
            }}
        >
            <div className='ct-imagecard-inner-wrapper'>
                {cardImage?
                    (<span className={'ct-imagecard-image'} style={{color: imageColor}}>
                        {cardImage}
                    </span>)
                    :
                    <></>
                }
                
                <div className={'ct-imagecard-title'}>
                    {cardTitle}
                </div>
                <div className={'ct-imagecard-description'}>
                    {cardDescription}
                </div>
                {children}
            </div>
        </Card>
    )
}

export default CTImageCard
