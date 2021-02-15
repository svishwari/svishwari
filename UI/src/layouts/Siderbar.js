import "./Sidebar.scss";
import React from "react";


export const Sidebar = ({ width, height, children, collapsed }) => {
  
  return (
    <React.Fragment>
      <div
        className={"side-bar " + (collapsed ? 'collapsed' : '')} 
        style={{
          width: width,
          minHeight: '100vh'
        }}
      >
        <div className="content">{children}</div>
      </div>
    </React.Fragment>
  );
};