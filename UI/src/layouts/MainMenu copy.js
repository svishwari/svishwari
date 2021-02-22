import React from "react";
import { NavLink, withRouter } from "react-router-dom";
import routeDefinitions from "./mainMenu.json";
import "./MainMenu.scss";

const getNavLinkClass = (path) =>
  this.props.location.pathname === path ? "active" : "";

const MainMenu = withRouter((props) => {
  const MenuItems = routeDefinitions.map((route, key) =>
    route.subItems && route.subItems.length > 0 ? (
      <ul key={`sub_${key}`} title={route.name}>
        {route.subItems.map((subItem, key) => (
          <li>
            <div>
              <NavLink exact activeClassName="active" to={subItem.path}>
                <span className="iconify" data-icon={`mdi:${subItem.icon}`} />
                <span className="text">{subItem.name}</span>
              </NavLink>
            </div>
          </li>
        ))}
      </ul>
    ) : (
      <li key={`main_${key}`}>
        <div>
          <NavLink exact activeClassName="active" to={route.path}>
            <span className="iconify" data-icon={`mdi:${route.icon}`} />
            <span className="text">{route.name}</span>
          </NavLink>
        </div>
      </li>
    )
  );
  return (
    <>
      <div className="menuWrapper">
        <h3 className="text">Navigation</h3>
        <ul className="menu">{MenuItems}</ul>
      </div>
    </>
  );
});

export default MainMenu;
