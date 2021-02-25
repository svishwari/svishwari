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
    <div className="app-header ">
      <Collapse onClick={() => toggle()} className={`trigger ${props.collapsed ? 'extra-space' : ''}`} />
      <UserAvatar username={props.userInfo.name} />
      {/* <span>{props.userInfo.name}</span> */}
    </div>
  );
};

const mapStateToProps = (state) => ({
  userInfo: state.user.loggedInUser || [],
});

export default connect(mapStateToProps)(TopHeader);
