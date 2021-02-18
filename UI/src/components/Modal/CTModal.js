import React, { useState } from 'react';
import './CTModal.scss';
import Dialog from '@material-ui/core/Dialog';

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
        screens=[],
        showFooter=true,
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
        
        handleChangeScreen();
        onPreviousScreen();
    }
    
    const handleNextScreen = () => {
        if (activeScreenIndex !== screens.length - 1) { 
            setActiveScreenIndex(activeScreenIndex + 1); 
        }
        handleChangeScreen();
        onNextScreen();
    }
    
    const handleChangeScreen = () => {
        onChangeScreen();
    }
    
    const handleComplete = () => {
        onComplete();
    }
    
    return (
        <Dialog
            open={open}
            onClose={handleClose}
            className='ct-modal-wrapper'
            {...props}
        >
            {/* Modal Header */}
            <div className="modal-header">
                {/* Close Button */}
                {showCloseButton &&
                    <div onClick={handleClose}>X</div>
                }

                {/* Indicators */}
                {showIndicators && screens.map((screen, index) => 
                    <div className={`indicator ${activeScreenIndex === index ? 'active' : ''}`}>{index}</div>
                )}
            </div>

            {/* Modal Body */}
            <div className="modal-body">
                {/* Active Screen */}
                {screens[activeScreenIndex]}
            </div>
            
            {/* Modal Footer */}
            {showFooter &&
                <div className="modal-footer">
                    <div className="modal-footer-left">
                        { activeScreenIndex > 0 && <span onClick={handlePreviousScreen}>{ props.backButton }</span> }
                        { footerLeftButtons.map(button => button) }
                    </div>
                    <div className="modal-footer-right">
                        { footerRightButtons.map(button => button) }
                        { activeScreenIndex < screens.length - 1 && <span onClick={handleNextScreen}>{ props.nextButton }</span> }
                        { activeScreenIndex === screens.length - 1 && <span onClick={handleComplete}>{ props.completeButton }</span> }
                    </div>
                </div>
            }
        </Dialog>
    )
}

export default CTModal
