import React, { useState } from "react";
import "./CTModal.scss";
import Dialog from "@material-ui/core/Dialog";
import CTSecondaryButton from "../Button/CTSecondaryButton";
import CTPrimaryButton from "../Button/CTPrimaryButton";

// To use this component you need to create a reference to the CTModal
// and call it's handle open function
// For more details visit: https://reactjs.org/docs/hooks-reference.html#useref

const CTModal = React.forwardRef((props, ref) => {
  const [open, setOpen] = useState(props.isOpen);
  const [activeScreenIndex, setActiveScreenIndex] = useState(0);

  const handleClose = () => {
    setOpen(false);
    props.onClose();
    setActiveScreenIndex(0);
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
    if (activeScreenIndex !== props.screens.screenComponents.length - 1) {
      setActiveScreenIndex(activeScreenIndex + 1);
    } else {
      handleClose();
    }
    handleChangeScreen();
    props.screens.righButtonFunctions[activeScreenIndex]();
    props.onNextScreen();
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
        {/* Close Button */}
        {props.showCloseButton && <div onClick={handleClose}>X</div>}

        {/* Indicators */}
        {IS_MULTI_MODAL &&
          props.showIndicators &&
          props.screens.screenComponents.map((screen, index) => (
            <div
              key={index}
              className={`indicator ${
                activeScreenIndex === index ? "active" : ""
              }`}
            />
          ))}
      </div>

      {/* Modal Body */}
      <div className="modal-body">
        {/* Active Screen */}
        <div className="ct-modal-title">{props.modalTitle}</div>
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
            {props.footerLeftButtons}
          </div>
          <div className="modal-footer-right">
            {props.footerRightButtons}
            {IS_MULTI_MODAL && (
              <CTPrimaryButton onClick={handleNextScreen}>
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
  showCloseButton: false,
  showIndicators: true,
  onClose: () => void 0,
  onNextScreen: () => void 0,
  onPreviousScreen: () => void 0,
  onChangeScreen: () => void 0,
  onComplete: () => void 0,
  screens: {},
  showFooter: true,
  mainCTAText: "Complete",
  backButton: "Back",
  completeButton: "Finish",
  maxWidth: "md",
  footerLeftButtons: [],
  footerRightButtons: [],
};
