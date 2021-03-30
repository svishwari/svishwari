import React, { useState } from "react";
import "./CTModal.scss";
import Dialog from "@material-ui/core/Dialog";
import { useDispatch } from "react-redux";
import CTSecondaryButton from "../Button/CTSecondaryButton";
import CTPrimaryButton from "../Button/CTPrimaryButton";
import { hideModal } from "../../modules/modal/action";

// Opening and closing has been made dynamic using redux, so it can be opened or closed from anywhere
// Incase of closeing the modal from outside using dipatch onClose function is not going to work

const CTModal = React.forwardRef((props, ref) => {
  const [open, setOpen] = useState(true);
  const [activeScreenIndex, setActiveScreenIndex] = useState(props.startScreenNumber);

  const dispatch = useDispatch();

  const handleClose = () => {
    setOpen(false);
    props.onClose();
    dispatch(hideModal());
  };

  const handlePreviousScreen = () => {
    if (activeScreenIndex !== 0) {
      setActiveScreenIndex(activeScreenIndex - 1);
    } else {
      handleClose();
    }

    handleChangeScreen();
    props.onPreviousScreen();
  };

  const handleNextScreen = () => {
    if(!props.screens.rightButtonProps[activeScreenIndex].isDisabled){
      if (activeScreenIndex !== props.screens.screenComponents.length - 1) {
        setActiveScreenIndex(activeScreenIndex + 1);
      } else {
        handleClose();
      }
      handleChangeScreen();
      props.screens.righButtonFunctions[activeScreenIndex]();
      props.onNextScreen();
    }
  };

  const handleChangeScreen = () => {
    props.onChangeScreen();
  };

  const handleComplete = () => {
    props.onComplete();
    handleClose();
  };

  const IS_MULTI_MODAL = Object.keys(props.screens).length !== 0;

  React.useImperativeHandle(ref, () => ({
    handleOpen() {
      setOpen(true);
    },
  }));

  return (
    <Dialog
      open={open}
      onClose={handleClose}
      className="ct-modal-wrapper"
      fullWidth
      maxWidth={props.maxWidth}
    >
      {/* Modal Header */}
      <div className="modal-header">

        {/* Indicators */}
        {IS_MULTI_MODAL &&
          props.showIndicators &&
          props.screens.screenComponents.map((screen, index) => (
            <div
              key={props.screens.righButtonNames[index]}
              className={`indicator ${
                activeScreenIndex === index && "active"
              }
              ${ activeScreenIndex < index && "to-be-done"}
              `}
            />
          ))}
      </div>

      {/* Modal Body */}
      <div className="modal-body">
        {/* Active Screen */}
        <div className="ct-modal-title">{props.modalTitle}</div>
        {IS_MULTI_MODAL && <div className="ct-modal-subtitle">{props.screens.screenTitle[activeScreenIndex]}</div>}
        <div className="ct-modal-subtitle">{props.modalSubtitle}</div>
        <div className="ct-modal-body">{props.modalBody}</div>
        {IS_MULTI_MODAL && props.screens.screenComponents[activeScreenIndex]}
      </div>

      {/* Modal Footer */}
      {props.showFooter && (
        <div className="modal-footer">
          <div className="modal-footer-left">
            {!IS_MULTI_MODAL && (
              <CTSecondaryButton onClick={handleClose}>
                Cancel
              </CTSecondaryButton>
            )}
            {IS_MULTI_MODAL && (
              <CTSecondaryButton onClick={handlePreviousScreen}>
                {activeScreenIndex === 0 ? "Close" : props.backButton}
              </CTSecondaryButton>
            )}
            {props.footerLeftButtons.map(each => {
              if( activeScreenIndex === each.props.activeindex){
                return each;
              }
              return "";
            })}
          </div>
          <div className="modal-footer-right">
            {props.footerRightButtons}
            {IS_MULTI_MODAL && (
              <CTPrimaryButton
                {...props.screens.rightButtonProps[activeScreenIndex]}
                onClick={handleNextScreen}
                >
                {props.screens.righButtonNames[activeScreenIndex]}
              </CTPrimaryButton>
            )}
            {!IS_MULTI_MODAL && (
              <CTPrimaryButton onClick={handleComplete}>
                {props.mainCTAText}
              </CTPrimaryButton>
            )}
          </div>
        </div>
      )}
    </Dialog>
  );
});

export default CTModal;

CTModal.defaultProps = {
  isOpen: false,
  showIndicators: true,
  onClose: () => undefined,
  onNextScreen: () => undefined,
  startScreenNumber: 0,
  onPreviousScreen: () => undefined,
  onChangeScreen: () => undefined,
  onComplete: () => undefined,
  screens: {
    // ************************
    // This prop accepts the following items and each item is a required one
    // and all the sub props need to be of same length
    // ************************
    // screenComponents: [],
    // rightButtonProps: [],
    // righButtonNames: [],
    // righButtonFunctions: [],
    // screenTitle: [],
  },
  showFooter: true,
  mainCTAText: "Complete",
  backButton: "Back",
  completeButton: "Finish",
  maxWidth: "md",
  footerLeftButtons: [],
  footerRightButtons: [],
};
