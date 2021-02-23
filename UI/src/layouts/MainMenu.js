import React from "react";
import { Nav, NavDropdown } from "react-bootstrap";
import { NavLink, withRouter, useLocation } from "react-router-dom";
import routeDefinitions from "./mainMenu.json";
import "./MainMenu.scss";

const navItem = (route) => (
  <NavLink exact activeClassName="active" to={route.path}>
    <span className="iconify" data-icon={`mdi:${route.icon}`} />
    <span className="text">{route.name}</span>
    {/* {badge ? } */}
  </NavLink>
);

const MainMenu = withRouter(() => {
  const location = useLocation();
  const exactRoute = (path) =>
    (path !== "/" && location.pathname.includes(path)) ||
    path === location.pathname
      ? "active"
      : "";
  const openDropDown = (path) => location.pathname.includes(path);
  const MenuItems = routeDefinitions.map((route) =>
    route.subItems && route.subItems.length > 0 ? (
      <NavDropdown
        title={navItem(route)}
        id="nav-dropdown"
        key={`${Math.random().toString(36).substr(2, 36)}`}
        show={openDropDown(route.path)}
        className={exactRoute(route.path)}
      >
        {route.subItems.map((subItem) => (
          <div>
            <NavDropdown.Item
              className={exactRoute(subItem.path)}
              key={`${Math.random().toString(36).substr(2, 36)}`}
            >
              {navItem(subItem)}
            </NavDropdown.Item>
          </div>
        ))}
      </NavDropdown>
    ) : (
      <Nav.Link key={`${Math.random().toString(36).substr(2, 36)}`} className={exactRoute(route.path)}>
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
