// React imports
import React from "react";

// Stylesheet
import "./CTTertiaryButton.scss";

const CTTertiaryButton = ({
  onClickFn,
  customClass = "",
  isDisabled = false,
  isLoading = false,
  btnWidth = 160,
  btnHeight = 40,
  children,
  ...props
}) => (
  <button
    style={{ width: btnWidth, height: btnHeight }}
    className={
      isDisabled
        ? `ct-btn-tertiary-disabled ${customClass}`
        : `ct-btn-tertiary ${customClass}`
    }
    onClick={isDisabled ? undefined : onClickFn}
    {...props}
  >
    {children}
  </button>
);

export default CTTertiaryButton;
