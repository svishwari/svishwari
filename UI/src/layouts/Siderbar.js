import "./Sidebar.scss";
import React from "react";

export const Sidebar = ({ width, children, collapsed }) => (
  <>
    <div
      className={`side-bar ${collapsed ? "collapsed" : ""}`}
      style={{
        width,
        minHeight: "100vh",
      }}
    >
      <div className="content">{children}</div>
    </div>
  </>
);

export default Sidebar;
