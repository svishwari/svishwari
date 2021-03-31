import { AppBar } from '@material-ui/core';
import React from 'react';
import { connect } from 'react-redux';
import { ReactComponent as Collapse } from '../assets/icons/collapse.svg';
import { UserAvatar } from '../components/UserAvatar';
import './topHeader.scss';

const TopHeader = (props ) => {
  const toggle = () => {
    props.isCollapsed();
  };
  return (
    <AppBar position="static"
      className={props.collapsed ? 'app-header collapsed': 'app-header'}>
      <Collapse onClick={() => toggle()} className={`trigger ${props.collapsed ? 'extra-space' : ''}`} />
      <UserAvatar username={props.userInfo.name} />
    </AppBar>  );
};

const mapStateToProps = (state) => ({
  userInfo: state.user.loggedInUser || [],
});

export default connect(mapStateToProps)(TopHeader);
