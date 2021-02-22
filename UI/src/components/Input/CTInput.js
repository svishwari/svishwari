import React from "react";
import "./CTInput.scss";

const CTInput = ({
  onChangeFunc,
  inputType = "text",
  placeholder = "Please enter some input",
  inputWidth = "100%",
  errorMessage = "",
  ...props
}) => (
  <span className="ct-input-wrapper">
    <input
      className={errorMessage !== "" ? "input-error-ct" : ""}
      type={inputType}
      placeholder={placeholder}
      style={{ width: inputWidth }}
      onChange={onChangeFunc}
      {...props}
    />
    <div className="input-error-ct-message">{errorMessage}</div>
  </span>
);

export default CTInput;
