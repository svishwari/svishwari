//React imports
import React from 'react';

//Stylesheet
import './CTSecondaryButton.scss';

const CTSecondaryButton = ({onClickFn,customClass='',isDisabled=false, isLoading=false,btnWidth=160,btnHeight=40,  children, ...props}) => {
    return (
        <button 
            style={{width: btnWidth,height: btnHeight}} 
            className={isDisabled ? `ct-btn-secondary-disabled ${customClass}`: `ct-btn-secondary ${customClass}`}
            onClick={isDisabled ? undefined :onClickFn}
            {...props}
            >
                {children}
        </button>
    )
}

export default CTSecondaryButton;