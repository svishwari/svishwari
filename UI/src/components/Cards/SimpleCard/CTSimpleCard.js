import React from "react";
import Card from "react-bootstrap/Card";
import "./CTSimpleCard.scss";

const CTSimpleCard = ({
  cardComponent,
  onClickFn,
  width = "100%",
  customClass = "",
  children,
  ...props
}) => (
  <Card
    onClick={onClickFn}
    className={`ct-card-wrapper ${customClass}`}
    {...props}
    style={{ width }}
  >
    {cardComponent}
    {children}
  </Card>
);

export default CTSimpleCard;
