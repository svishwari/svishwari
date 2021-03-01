import React, { useState } from 'react';
import { useOktaAuth } from '@okta/okta-react';
import { useDispatch } from 'react-redux';
import { ThemeProvider } from '@material-ui/core';

import './PrivateLayout.scss';

import TopHeader from './topHeader';
import ModalRoot from '../modules/modal/ModalRoot';
import LeftNav from './leftNav';
import theme from './theme';

const setUser = (payload) => ({
  type: 'updateLoggedInUser',
  payload,
});

// import CTToast from '../components/Toast/CTToast';

export const PrivateLayout = ({ children }) => {
  const [collapsed, setCollapseState] = useState(false);
  const { authState, oktaAuth } = useOktaAuth();
  const disptach = useDispatch();

  React.useEffect(() => {
    if (authState.isAuthenticated) {
      oktaAuth.getUser().then((info) => {
        disptach(setUser(info));
      });
    }
  }, []);

  return (
    <ThemeProvider theme={theme}>
      <div className="dash-layout">
        <div className="toast-container">
          {/* <CTToast toastType='success' toastMessage="This is an error or alert! It will disappear in 5 seconds on its own."/>
          <CTToast toastType='error' toastMessage="This is an error or alert! It will disappear in 5 seconds on its own."/> */}
        </div>
        <LeftNav collapsed={collapsed} />
        <div className="wrapper">
          <TopHeader
            isCollapsed={() => {
              setCollapseState(!collapsed);
            }}
            collapsed={collapsed}
          />
          <div className="content">{children}</div>
        </div>
        <ModalRoot />
      </div>
    </ThemeProvider>
  );
};

export default PrivateLayout;
