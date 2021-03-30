import React from "react";
import Card from "react-bootstrap/Card";
import "./CTSimpleCard.scss";

const CTSimpleCard = ({
  cardComponent,
  onClickFn,
  customClass = "",
  children,
  ...props
}) => (
  <Card
    onClick={onClickFn}
    className={`ct-card-wrapper ${customClass}`}
    {...props}
  >
    {cardComponent}
    {children}
  </Card>
);

export default CTSimpleCard;
