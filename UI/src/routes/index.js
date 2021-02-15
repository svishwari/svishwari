import React, { useEffect } from "react";
import {
  Route,
  Switch,
  useHistory,
  withRouter,
  useLocation,
  // Redirect,
} from "react-router-dom";

// Auth
import { OktaAuth } from "@okta/okta-auth-js";
import { oktaAuthConfig } from "../modules/auth/AuthConfig";
import { Security, SecureRoute, LoginCallback } from "@okta/okta-react";

//Modules
import Dashboard from "../modules/dashboard/Dashboard";
import Page from "../pages/Page";
import LoggedInRedirect from "../modules/auth/LoggedInRedirect";

// Layouts
import { PrivateLayout } from "../layouts/PrivateLayout";
import { StyleGuide } from "../pages/StyleGuide";

const oktaAuth = new OktaAuth(oktaAuthConfig);

function Routes() {
  const { pathname } = useLocation();
  const history = useHistory();

  const onAuthRequired = () => {
    history.push("/login");
  };

  useEffect(() => {
    let _appTitle = " | HUX Unified Solution";
    document.body.classList.add("loaded");

    let route = history.location.pathname;
    switch (route) {
      case "/":
        _appTitle = "Home" + _appTitle;
        break;
      default:
        break;
    }
    document.title = _appTitle;
    window.scrollTo(0, 0);
  }, [pathname]);
  useEffect(() => {}, []);

  return (
    <div>
      <Security oktaAuth={oktaAuth} onAuthRequired={onAuthRequired}>
        <SecureRoute path="/:path?" exact>
          <Switch>
            <PrivateLayout>
              <Switch>
                <Route path="/" exact component={Dashboard} />
                <Route path="/styleguide" exact component={StyleGuide} />
                <Route path="/orchestration" exact component={Page} />
                <Route path={"/orchestration?/:path?"} exact>
                  <Switch>
                    <Route
                      path="/audiences"
                      exact
                      component={Dashboard}
                    />
                  </Switch>
                </Route>
              </Switch>
            </PrivateLayout>
          </Switch>
        </SecureRoute>
        <Route path="/login" render={() => <LoggedInRedirect />} />
        <Route path="/login/callback" component={LoginCallback} />
      </Security>
    </div>
  );
}

export default withRouter(Routes);
