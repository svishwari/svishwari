import { React } from "react";
import { ReactComponent as AppLogo } from "../assets/logo.svg";
import "./leftNav.scss";
import { Sidebar } from "./Siderbar";
import MainMenu from "./MainMenu";

const LeftNav = ({ collapsed }) => (
  <Sidebar width="280" height="100" collapsed={collapsed}>
    <div className="borderShadow" />
    <AppLogo className="appLogo" />
    <MainMenu />
    <div className="poweredBy">
      <AppLogo />
      <span>Hux by Deloitte</span>
    </div>
  </Sidebar>
);

export default LeftNav;
