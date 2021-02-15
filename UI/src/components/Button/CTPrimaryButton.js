//React imports
import React from 'react';

//Stylesheet
import './CTPrimaryButton.scss';

const CTPrimaryButton = ({onClickFn, customClass='',isDisabled=false, isLoading=false,btnWidth=160,btnHeight=40,children, ...props }) => {
    return (
        <button 
            style={{width: btnWidth,height: btnHeight}} 
            className={isDisabled ? `ct-btn-primary-disabled ${customClass}`: `ct-btn-primary ${customClass}`}
            onClick={isDisabled ? undefined :onClickFn}
            {...props}
            >
                {children}
        </button>
    )
}

export default CTPrimaryButton;
