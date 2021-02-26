import React from "react";
import "./CTPopover.scss";
import { OverlayTrigger, Popover } from "react-bootstrap";

const CTPopover = ({ popoverContent,customClass, children, ...props }) => {
  const popover = (
    <Popover className={`ct-popover-wrapper ${customClass}`}>
      <Popover.Content>{popoverContent}</Popover.Content>
    </Popover>
  );
  return (
    <OverlayTrigger
      trigger="click"
      placement="bottom"
      overlay={popover}
      rootClose
      {...props}
    >
      {children}
    </OverlayTrigger>
  );
};

export default CTPopover;
