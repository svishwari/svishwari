/**
 * Selectors for DOM elements in the application.
 */
export default {
  home: {
    signin: "[data-e2e='signin']",
  },
  login: {
    email: "[id=okta-signin-username]",
    password: "[id=okta-signin-password]",
    submit: "[id=okta-signin-submit]",
  },
  datasources: "[data-e2e='dataSourcesList']",
  destinations: "[data-e2e='destinationsList']",
  dataSourcesAdd: "[tabindex='0'][data-e2e='dataSourcesAddList']",
  connections: "a[href='/connections']",
  addDataSource: "a[href='/datasources/add?select=true']",
}
