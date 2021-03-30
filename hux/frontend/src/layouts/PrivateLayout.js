import React, { useState } from 'react';
import { useOktaAuth } from '@okta/okta-react';
import { useDispatch } from 'react-redux';
import { CssBaseline, ThemeProvider } from '@material-ui/core';

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
        <CssBaseline />
        <TopHeader
          isCollapsed={() => {
            setCollapseState(!collapsed);
          }}
          collapsed={collapsed}
        />
        <div className="wrapper">
          <LeftNav collapsed={collapsed} />
          <main className="content">{children}</main>
        </div>
        <ModalRoot />
      </div>
    </ThemeProvider>
  );
};

export default PrivateLayout;
