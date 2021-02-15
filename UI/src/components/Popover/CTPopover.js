import React from 'react';
import './CTPopover.scss';
import { OverlayTrigger, Popover } from "react-bootstrap";

const CTPopover = ({popoverContent,children,...props}) => {

    const popover = (
        <Popover className='ct-popover-wrapper'>
          <Popover.Content>
            {popoverContent}
          </Popover.Content>
        </Popover>
    );
    return (
        <OverlayTrigger
            trigger="click"
            placement="bottom"
            overlay={popover}
            rootClose={true}
            {...props}
        >
            {children}
      </OverlayTrigger>
    )
}

export default CTPopover
