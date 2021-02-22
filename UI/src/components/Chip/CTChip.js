import React from "react";
import { Chip, IconButton } from "@material-ui/core";
import "./CTChip.scss";

const CTChip = ({
  hasIcons = true,
  isWorkingFn,
  isNotWorkingFn,
  isWorking = true,
  children,
}) => (
  <div className="ct-chip-wrapper">
    <Chip
      label={children}
      className={`${isWorking ? "ct-chip-success" : "ct-chip-not-success"}`}
    />
    {hasIcons ? (
      isWorking === true ? (
        <IconButton onClick={() => isWorkingFn()}>
          <span
            className="iconify ct-chip-success-icon"
            data-icon="mdi:refresh-circle"
            data-inline="false"
          />
        </IconButton>
      ) : (
        <IconButton onClick={() => isNotWorkingFn()}>
          <span
            className="iconify ct-chip-not-success-icon"
            data-icon="mdi:arrow-right-circle"
            data-inline="false"
          />
        </IconButton>
      )
    ) : (
      <></>
    )}
  </div>
);

export default CTChip;
