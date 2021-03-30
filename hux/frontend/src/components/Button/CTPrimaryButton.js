// React imports
import React from "react";

// Stylesheet
import "./CTPrimaryButton.scss";

const CTPrimaryButton = ({
  onClickFn,
  customClass = "",
  isDisabled = false,
  btnWidth = 160,
  btnHeight = 40,
  children,
  ...props
}) => (
  <button
    style={{ minWidth: btnWidth, minHeight: btnHeight }}
    className={
      isDisabled
        ? `ct-btn-primary-disabled ${customClass}`
        : `ct-btn-primary ${customClass}`
    }
    type='button'
    onClick={isDisabled ? undefined : onClickFn}
    {...props}
  >
    {children}
  </button>
);

export default CTPrimaryButton;
