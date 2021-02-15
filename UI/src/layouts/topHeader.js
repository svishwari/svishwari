import React from "react";
import { ReactComponent as Collapse } from "../assets/icons/collapse.svg";
import { UserAvatar } from "../components/UserAvatar";
import "./topHeader.scss";

const TopHeader = ({ isCollapsed, collapsed }) => {
  const toggle = () => {
    isCollapsed();
  };
  return (
    <div className="app-header ">
      <Collapse onClick={() => toggle()} className={"trigger " + (collapsed ? 'extra-space' : '')} />
      <UserAvatar username={"Rahul Goel"}/>
    </div>
  );
};

export default TopHeader;
