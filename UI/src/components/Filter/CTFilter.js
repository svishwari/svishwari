import React from "react";
import "./CTFilter.scss";
import CTPopover from "../Popover/CTPopover";


// THIS IS A TODO FILE
// MOST OF THE FUNCTIONALITY STILL NEEDS TO BE CHANGED
const CTFilter = (
) => {

  const filterContent = (
    <div>
      Filter content
    </div>
  );

  return (
    <CTPopover popoverContent={filterContent}>
      <div className="ct-filter-wrapper">
        <span className="iconify" data-icon="mdi:filter" data-inline="false" />
      </div>
    </CTPopover>
  );
};

export default CTFilter;
