import React from 'react';
import './CTLabel.scss';

const CTLabel = ({children, ...props}) => {
    return (
        <div className='ct-label-wrapper'>
            <label {...props}>
                {children}
            </label>
        </div>
    )
}

export default CTLabel
