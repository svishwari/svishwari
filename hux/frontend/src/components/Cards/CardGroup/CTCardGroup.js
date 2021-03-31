import React from "react";
import "./CTCardGroup.scss";

const CardWrapper = ({ children, ...props }) => (
  <div className="ct-card-group-wrapper" {...props}>
    {children}
  </div>
);

export default CardWrapper;
