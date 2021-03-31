// React imports
import React from "react";

// Stylesheet
import "./CTSecondaryButton.scss";

const CTSecondaryButton = ({
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
        ? `ct-btn-secondary-disabled ${customClass}`
        : `ct-btn-secondary ${customClass}`
    }
    onClick={isDisabled ? undefined : onClickFn}
    type='button'
    {...props}
  >
    {children}
  </button>
);

export default CTSecondaryButton;
