import React from "react";
import { Dropdown, OverlayTrigger, Popover } from "react-bootstrap";
import { useOktaAuth } from "@okta/okta-react";
import './UserAvatar.scss';
export const UserAvatar = ({ username }) => {
  const { oktaAuth } = useOktaAuth();
  // oktaAuth.getUser().then(info => {
  //   console.log(info)
  // });

  const getInitials = (name) => {
    return name.toString().match(/(^\S\S?|\b\S)?/g).join("").match(/(^\S|\S$)?/g).join("").toUpperCase()
  }
  const popover = (
    <Popover id="user-menu" className="userAvatarMenu">
      <Popover.Content>
        <Dropdown.Item>My Account</Dropdown.Item>
        <Dropdown.Item
          onClick={() => {
            oktaAuth.signOut();
          }}
        >
          Log Out
        </Dropdown.Item>
      </Popover.Content>
    </Popover>
  );
  return (
    <OverlayTrigger
      trigger="click"
      placement="bottom"
      overlay={popover}
      rootClose={true}
    >
      
      <div className="userAvatarIcon"><span className="avatar">{getInitials(username)}</span><button variant="light" className="btn">{username} <span className="iconify" data-icon="mdi:chevron-down"></span></button></div>
    </OverlayTrigger>
  );
};
