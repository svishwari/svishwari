export default {
  oidc: {
    clientId: process.env.VUE_APP_OKTA_CLIENT_ID,
    issuer: process.env.VUE_APP_OKTA_ISSUER,
  },
  resourceUrl: process.env.VUE_APP_APIHOST,
  appTitle: "HUX Unified",
  endpoints: {},
  userDetails: "https://deloittedigital-ms.okta.com/enduser/settings",
}
