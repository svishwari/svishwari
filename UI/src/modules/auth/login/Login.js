import React, { useState } from "react";
import { useOktaAuth } from "@okta/okta-react";

import { ReactComponent as AppLogo } from "../../../assets/hux-logo-colored.svg";
import SideImage from "../../../assets/login-background.png";
import "./login.scss";

const Login = () => {
  const { oktaAuth } = useOktaAuth();
  const [sessionToken, setSessionToken] = useState();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [isError, setError] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();

    oktaAuth
      .signInWithCredentials({ username, password })
      .then((res) => {
        const { sessionToken } = res;
        setSessionToken(sessionToken);
        // sessionToken is a one-use token, so make sure this is only called once
        oktaAuth.signInWithRedirect({ sessionToken });
      })
      .catch((err) => setError(true));
  };

  const handleUsernameChange = (e) => {
    setUsername(e.target.value);
  };

  const handlePasswordChange = (e) => {
    setPassword(e.target.value);
  };

  if (sessionToken) {
    // Hide form while sessionToken is converted into id/access tokens
    return null;
  }

  return (
    <div className="login-wrapper">
      <div className="hidden-xs hidden-sm col-md-5 p-0 left-section">
        <img src={SideImage} alt="Logo" />
      </div>
      <div className="col-md-7 col-xs-12 p-0 right-section">
        <div className="login-form">
          <AppLogo />
          <h1>
            Access your <span className="color-360">360°</span> view
          </h1>
          <h6>
            Jump right in where you left off, and leave the hard work on us!
          </h6>

          <form onSubmit={handleSubmit} className="pb-4">
            {isError && <div className="error">Unable to Sign in</div>}
            <div className="form-group">
              <label>Email</label>
              <input
                id="username"
                type="text"
                value={username}
                autoComplete="true"
                onChange={handleUsernameChange}
              />
            </div>
            <div className="form-group">
              <label>Password </label>
              <input
                id="password"
                type="password"
                value={password}
                autoComplete="true"
                onChange={handlePasswordChange}
              />
            </div>
            <div>
              <input
                className="btn login-btn"
                id="submit"
                type="submit"
                value="Log In"
              />
            </div>
          </form>
          <div className="forgot-password">Forgot Password?</div>
        </div>
      </div>
    </div>
  );
};

export default Login;
