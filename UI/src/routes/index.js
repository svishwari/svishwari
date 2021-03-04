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
import { Security, SecureRoute, LoginCallback } from "@okta/okta-react";
import { oktaAuthConfig } from "../modules/auth/AuthConfig";

// Modules
import Dashboard from "../modules/dashboard/Dashboard";
import LoggedInRedirect from "../modules/auth/LoggedInRedirect";

// Layouts
import { PrivateLayout } from "../layouts/PrivateLayout";
// import { StyleGuide } from "../pages/StyleGuide";
import ConnectionsSummary from "../modules/connections/ConnectionsSummary";
import ComingSoon from "../pages/ComingSoon";
import DataSources from "../modules/connections/data-sources/DataSources";
import Destinations from "../modules/connections/destinations/Destinations";
import CustomersData from "../modules/customer-data/CustomersData";
import CustomerData from "../modules/customer-data/CustomerData";

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

    const route = history.location.pathname;
    switch (route) {
      case "/":
        _appTitle = `Home${_appTitle}`;
        break;
      default:
        break;
    }
    document.title = _appTitle;
    window.scrollTo(0, 0);
  }, [pathname]);
  useEffect(() => {}, []);

  return (
    <>
      <Security oktaAuth={oktaAuth} onAuthRequired={onAuthRequired}>
        <SecureRoute path="/:path?/:path?/:path?" exact>
          <Switch>
            <PrivateLayout>
              <Switch>
                <Route path="/" exact component={Dashboard} />
                <Route
                  path="/connections"
                  exact
                  component={ConnectionsSummary}
                />
                <Route
                  path="/connections/data-sources"
                  exact
                  component={DataSources}
                />
                <Route
                  path="/connections/destinations"
                  exact
                  component={Destinations}
                />
                <Route
                  path="/customer-profiles"
                  exact
                  component={CustomersData}
                />
                <Route
                  path="/customer-profiles/:profileID"
                  exact
                  component={CustomerData}
                />
                <Route path="*" exact component={ComingSoon} />
              </Switch>
            </PrivateLayout>
          </Switch>
        </SecureRoute>
        <Route path="/login" render={() => <LoggedInRedirect />} />
        <Route path="/login/callback" component={LoginCallback} />
      </Security>
    </>
  );
}

export default withRouter(Routes);
