import React, { useState } from 'react';
import './CTModal.scss';
import Dialog from '@material-ui/core/Dialog';
import CTSecondaryButton from '../Button/CTSecondaryButton';
import CTPrimaryButton from '../Button/CTPrimaryButton';

const CTModal = ({
        isOpen=true,
        showCloseButton=false,
        showIndicators=true,
        onOpen=() => void 0,
        onClose=() => void 0,
        onNextScreen=() => void 0,
        onPreviousScreen=() => void 0,
        onChangeScreen=() => void 0,
        onComplete=() => void 0,
        screens={},
        showFooter=true,
        mainCTAText='Complete',
        backButton='Back',
        completeButton='Finish',
        modalTitle,
        maxWidth='md',
        modalSubtitle,
        modalBody,
        footerLeftButtons=[],
        footerRightButtons=[],
        ...props
    }) => {
    
    const [open, setOpen] = useState(isOpen);
    const [activeScreenIndex, setActiveScreenIndex] = useState(0);
    
    const handleOpen = () => {
        setOpen(true);
        onOpen();
    }
    
    const handleClose = () => {
        setOpen(false);
        onClose();
    }
    
    const handlePreviousScreen = () => {
        if (activeScreenIndex !== 0) { 
            setActiveScreenIndex(activeScreenIndex - 1); 
        }
        else {
            handleClose();
        }
        
        handleChangeScreen();
        onPreviousScreen();
    }
    
    const handleNextScreen = () => {
        if (activeScreenIndex !== screens.screenComponents.length - 1) { 
            setActiveScreenIndex(activeScreenIndex + 1); 
        }
        else {
            handleClose();
        }
        handleChangeScreen();
        screens.righButtonFunctions[activeScreenIndex]();
        onNextScreen();
    }
    
    const handleChangeScreen = () => {
        onChangeScreen();
    }
    
    const handleComplete = () => {
        onComplete();
        handleClose();
    }

    const IS_MULTI_MODAL = Object.keys(screens).length !== 0;
    
    return (
        <Dialog
            open={open}
            onClose={handleClose}
            className='ct-modal-wrapper'
            fullWidth={true}
            maxWidth={maxWidth}
            {...props}
        >
            {/* Modal Header */}
            <div className="modal-header">
                {/* Close Button */}
                {showCloseButton &&
                    <div onClick={handleClose}>X</div>
                }

                {/* Indicators */}
                {IS_MULTI_MODAL && showIndicators && screens.screenComponents.map((screen,index) => 
                    <div key={index} className={`indicator ${activeScreenIndex === index ? 'active' : ''}`}></div>
                )}
            </div>

            {/* Modal Body */}
            <div className="modal-body">
                {/* Active Screen */}
                <div className='ct-modal-title'>
                    {modalTitle}
                </div>
                <div className='ct-modal-subtitle'>
                    {modalSubtitle}
                </div>
                <div className='ct-modal-body'>
                    {modalBody}
                </div>
                {IS_MULTI_MODAL && screens.screenComponents[activeScreenIndex]}
            </div>
            
            {/* Modal Footer */}
            {showFooter &&
                <div className="modal-footer">
                    <div className="modal-footer-left">
                        { !IS_MULTI_MODAL && <CTSecondaryButton onClick={handleClose}>Cancel</CTSecondaryButton>}
                        { IS_MULTI_MODAL && <CTSecondaryButton onClick={handlePreviousScreen}>{activeScreenIndex===0 ? 'Close' : backButton}</CTSecondaryButton> }
                        { footerLeftButtons}
                    </div>
                    <div className="modal-footer-right">
                        {footerRightButtons}
                        { IS_MULTI_MODAL && <CTPrimaryButton onClick={handleNextScreen}>{screens.righButtonNames[activeScreenIndex] }</CTPrimaryButton>}
                        { !IS_MULTI_MODAL && <CTPrimaryButton onClick={handleComplete}>{ mainCTAText }</CTPrimaryButton> }
                    </div>
                </div>
            }
        </Dialog>
    )
}

export default CTModal
