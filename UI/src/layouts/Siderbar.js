import './Sidebar.scss';
import React from 'react';
import classNames from 'classnames';
import { Drawer } from '@material-ui/core';

export const Sidebar = ({ width, children, collapsed }) => 
  // const container = window !== undefined ? () => document.getElementById("main-menu") : undefined;
   (
    <nav aria-label="main-menu" id="main-menu">
      <Drawer
        open
        variant="persistent"
        classes={{
          paper: classNames({
            'side-bar': true,
            collapsed,
          }),
        }}
        className={`side-bar ${collapsed ? 'collapsed' : ''}`}
        style={{
          width,
          minHeight: '100vh',
        }}
      >
        <div className="content">{children}</div>
      </Drawer>
    </nav>
  )
;

export default Sidebar;
