import React, { useState } from "react";
import "./PrivateLayout.scss";

import LeftNav from "./leftNav";

import TopHeader from "./topHeader";

// import CTToast from '../components/Toast/CTToast';

export const PrivateLayout = ({ children }) => {
  const [collapsed, setCollapseState] = useState(false);

  return (
    <div className="dash-layout">
      <div className="toast-container">
        {/* <CTToast toastType='success' toastMessage="This is an error or alert! It will disappear in 5 seconds on its own."/>
          <CTToast toastType='error' toastMessage="This is an error or alert! It will disappear in 5 seconds on its own."/> */}
      </div>
      <LeftNav collapsed={collapsed} />
      <div className="wrapper">
        <TopHeader
          isCollapsed={(e) => {
            setCollapseState(!collapsed);
          }}
          collapsed={collapsed}
        />
        <div className="content">{children}</div>
      </div>
    </div>
  );
};
