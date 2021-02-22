import React from "react";
import { Nav, NavDropdown } from "react-bootstrap";
import { NavLink, withRouter, useLocation } from "react-router-dom";
import routeDefinitions from "./mainMenu.json";
import "./MainMenu.scss";

const navItem = (route, badge) => (
  <NavLink exact activeClassName="active" to={route.path}>
    <span className="iconify" data-icon={`mdi:${route.icon}`} />
    <span className="text">{route.name}</span>
    {/* {badge ? } */}
  </NavLink>
);

const MainMenu = withRouter((props) => {
  const location = useLocation();
  const exactRoute = (path) =>
    (path !== "/" && location.pathname.includes(path)) ||
    path === location.pathname
      ? "active"
      : "";
  const openDropDown = (path) => location.pathname.includes(path);
  const MenuItems = routeDefinitions.map((route, rkey) =>
    route.subItems && route.subItems.length > 0 ? (
      <NavDropdown
        title={navItem(route)}
        id="nav-dropdown"
        key={`submenu_${rkey}`}
        show={openDropDown(route.path)}
        className={exactRoute(route.path)}
      >
        {route.subItems.map((subItem, skey) => (
          <div>
            <NavDropdown.Item
              className={exactRoute(subItem.path)}
              key={`${route.name.toString().toLowerCase()}_${skey}`}
            >
              {navItem(subItem)}
            </NavDropdown.Item>
          </div>
        ))}
      </NavDropdown>
    ) : (
      <Nav.Link key={`main_${rkey}`} className={exactRoute(route.path)}>
        {navItem(route)}
      </Nav.Link>
    )
  );
  return (
    <div className="menuWrapper">
      <h3 className="text">Navigation</h3>
      <Nav className="mr-auto menu">{MenuItems}</Nav>
    </div>
  );
});

export default MainMenu;
