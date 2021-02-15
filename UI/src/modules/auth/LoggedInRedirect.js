import React from 'react';
import { Redirect } from 'react-router-dom';
import Login from './login/Login';
import { useOktaAuth } from '@okta/okta-react';
// import Signup from './signup/Signup';

const LoggedInRedirect = () => {
  const { authState } = useOktaAuth();

  if (authState.isPending) {
    return <div>Loading...</div>;
  }
  return authState.isAuthenticated ?
    <Redirect to={{ pathname: '/' }}/> :
    <Login />;
    // <Signup />;
};

export default LoggedInRedirect; 