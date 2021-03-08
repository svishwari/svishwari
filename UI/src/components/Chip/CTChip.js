import React, { useState } from "react";
import { Chip } from "@material-ui/core";
import { ReactComponent as RefreshCircle } from "../../assets/icons/refresh-circle.svg";
import { ReactComponent as ArrowRightCircle } from "../../assets/icons/arrow-right-circle.svg";
import "./CTChip.scss";

const CTChip = ({
  hasIcons = true,
  onClickFunc=()=>{},
  isWorking = true,
  isNotMiddle = true,
  children,
}) => {
  const [isHovered,setisHovered] = useState(false);

  const toggleHover = () => {
    setisHovered(!isHovered);
  }

  return (
  <div 
    className="ct-chip-wrapper"
    onKeyPress={onClickFunc}
    onClick={onClickFunc}
    onMouseOver={toggleHover} 
    onMouseOut={toggleHover} 
    onFocus={toggleHover}
    onBlur={toggleHover}
  >
    {
    isNotMiddle ?
    <>
      <Chip
        label={children}
        className={`${isWorking ? "ct-chip-success" : "ct-chip-not-success"} ${(isHovered && hasIcons) && "ct-chip-hover"}`}
      />
        {hasIcons ? (
          isWorking === true ? (
            <>
            <div className={`empty-space-container ${isHovered && "ct-s-hover"}`}/>
            <RefreshCircle
              className={`ct-chip-success-icon ${isHovered && "ct-chip-success-hover"}`}
              />
            </>
          ) : (
            <>
            <div className={`empty-space-container ${isHovered && "ct-ns-hover"}`}/>
            <ArrowRightCircle
              className={`ct-chip-not-success-icon ${isHovered && "ct-chip-not-success-hover"}`}
              />
            </>
          )
        ) : (
          <></>
        )}
      </> 
      : <>
        <Chip
          label={children}
          className={`ct-chip-middle ${isHovered && "ct-chip-middle-hover"}`}
        />
      </>
    }
  </div>
  
)};

export default CTChip;
