import React, { useState, useEffect } from "react";
import { ReactComponent as Collapse } from "../assets/icons/collapse.svg";
import { UserAvatar } from "../components/UserAvatar";
import "./topHeader.scss";
import { useOktaAuth } from "@okta/okta-react";

const TopHeader = ({ isCollapsed, collapsed }) => {
  const { authState, oktaAuth } = useOktaAuth();
  const [userInfo, setUserInfo] = useState({ name: "" });

  useEffect(() => {
    if (!authState.isAuthenticated) {
      // When user isn't authenticated, forget any user info
      setUserInfo(null);
    } else {
      oktaAuth.getUser().then((info) => {
        setUserInfo(info);
      });
    }
  }, [authState, oktaAuth]);

  const toggle = () => {
    isCollapsed();
  };
  return (
    <div className="app-header ">
      <Collapse
        onClick={() => toggle()}
        className={`trigger ${collapsed ? "extra-space" : ""}`}
      />
      <UserAvatar username={userInfo.name} />
    </div>
  );
};

export default TopHeader;
