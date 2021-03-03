/* eslint-disable no-unused-vars */
import {
  Collapse,
  List,
  ListItem,
  ListSubheader,
  ListItemIcon,
  ListItemText,
  makeStyles,
} from '@material-ui/core';
import React from 'react';
import { withRouter, useHistory, useLocation } from 'react-router-dom';
import routeDefinitions from './mainMenu.json';
import './MainMenu.scss';

const useStyles = makeStyles((theme) => ({
  root: {
    width: '100%',
  },
  nested: {
    paddingLeft: theme.spacing(4),
  },
  normal: {},
}));

const MainMenu = withRouter(() => {
  const classes = useStyles();
  const history = useHistory();
  const location = useLocation();

  const handleClick = (event) => {
    const route = event.currentTarget.attributes['data-to'].value;
    const isDropDown = Boolean(
      event.currentTarget.attributes['data-dropdown'] &&
        event.currentTarget.attributes['data-dropdown'].value,
    );
    history.push(route);
    if (isDropDown);
  };
  // const location = useLocation();
  const exactRoute = (path) =>
    (path !== '/' && location.pathname.includes(path)) || path === location.pathname
      ? 'active'
      : '';
  const open = (path) =>
    path !== '/' && (location.pathname.includes(path) || path === location.pathname);
  const navItem = (route, isChild, ix) => (
    <ListItem
      button
      data-to={route.path}
      key={`-key-nav-item-${route.id}`}
      className={`nav-link ${isChild ? 'nested' : ''} ${exactRoute(route.path)}`}
      onClick={handleClick}
    >
      <ListItemIcon className="icon-wrap">
        <span className="iconify" data-icon={`mdi:${route.icon}`} />
      </ListItemIcon>
      <ListItemText primary={route.name} />
      {isChild ? <span className="num">53</span> : <></>}
    </ListItem>
  );
  // const openDropDown = (path) => location.pathname.includes(path);
  const MenuItems = routeDefinitions.map((route, ix) =>
    route.subItems && route.subItems.length > 0 ? (
      <React.Fragment key={`-key-wrap-${route.id.toLowerCase()}`}>
        <ListItem
          button
          key={`-key-parent-${route.id.toLowerCase()}`}
          data-to={route.path}
          onClick={handleClick}
          data-dropdown="true"
          className={`nav-link ${exactRoute(route.path)}`}
        >
          <ListItemIcon className="icon-wrap">
            <span className="iconify" data-icon={`mdi:${route.icon}`} />
          </ListItemIcon>
          <ListItemText primary={route.name} />
        </ListItem>
        <Collapse
          in={open(route.path)}
          timeout="auto"
          unmountOnExit
          className={`sub-nav ${exactRoute(route.path)}`}
          key={`-key-collapse-${route.id.toLowerCase()}`}
        >
          <List component="div" className="sub-nav-list" disablePadding key={`-key-list-${route.id.toLowerCase()}`}>
            {route.subItems.map((subItem) => (
              <React.Fragment key={`-key-frag-${subItem.id.toLowerCase()}`}>
                {navItem(subItem, true)}
              </React.Fragment>
            ))}
          </List>
        </Collapse>
      </React.Fragment>
    ) : (
      <React.Fragment key={`-key-wrap-${route.id}`}>{navItem(route, false, ix)}</React.Fragment>
    ),
  );
  return (
    <List
      component="nav"
      aria-labelledby="nested-list-subheader"
      key="mainnavigation"
      subheader={
        <ListSubheader component="h3" id="nested-list-subheader" key="navigation">
          Navigation
        </ListSubheader>
      }
      className={`menuWrapper ${classes.root}`}
    >
      {MenuItems}
    </List>
  );
});

export default MainMenu;
