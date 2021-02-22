import React from "react";
import { Redirect } from "react-router-dom";
import { useOktaAuth } from "@okta/okta-react";
import Login from "./login/Login";
// import Signup from './signup/Signup';

const LoggedInRedirect = () => {
  const { authState } = useOktaAuth();

  if (authState.isPending) {
    return <div>Loading...</div>;
  }
  return authState.isAuthenticated ? (
    <Redirect to={{ pathname: "/" }} />
  ) : (
    <Login />
  );
  // <Signup />;
};

export default LoggedInRedirect;
