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

  // common components
  card: {
    title: "[data-e2e='card-title']",
    description: "[data-e2e='card-description']",
    },

  // navigation
  nav: {
    models: "[data-e2e='nav-models']",
  },

  // overview
  overview: {
    header: "[data-e2e='overview-header']",
    list: "[data-e2e='configuration-list']",
    item: "[data-e2e='configuration-item']",
    chart: "[data-e2e='overview-chart']",
  },

  // connections
  datasources: "[data-e2e='dataSourcesList']",
  destinations: "[data-e2e='destinationsList']",
  dataSourcesAdd: "[tabindex='0'][data-e2e='dataSourcesAddList']",
  connections: "a[href='/connections']",
  addDataSource: "[data-e2e='addDataSource']",

  // decisioning
  models: {
    header: "[data-e2e='models-header']",
    list: "[data-e2e='models-list']",
    item: "[data-e2e='model-item']",
  },

  //IDR
  idr: {
    identityResolution: "a[href='/identity-resolution']",
    overview: "[data-e2e='overviewList']",
    datafeed: "[data-e2e='datafeedtable']",
  },
}
