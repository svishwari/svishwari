import React from 'react';
import { Redirect } from 'react-router-dom';
import { useOktaAuth } from '@okta/okta-react';
import { useDispatch } from 'react-redux';
import Login from './login/Login';

const setUser = (payload) => ({
  type: 'updateLoggedInUser',
  payload,
});

// import Signup from './signup/Signup';

const LoggedInRedirect = () => {
  const { authState, oktaAuth } = useOktaAuth();
  const disptach = useDispatch();

  if (!authState.isAuthenticated) {
    disptach(setUser({}));
  } else {
    oktaAuth.getUser().then((info) => {
      disptach(setUser(info));
    });
  }

  if (authState.isPending) {
    return <div>Loading...</div>;
  }
  return authState.isAuthenticated ? <Redirect to={{ pathname: '/' }} /> : <Login />;
  // <Signup />;
};

export default LoggedInRedirect;
