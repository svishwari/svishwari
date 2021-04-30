export default {
  oidc: {
    clientId: process.env.VUE_APP_OKTA_CLIENT_ID,
    issuer: process.env.VUE_APP_OKTA_ISSUER,
  },
  resourceUrl: process.env.VUE_APP_API_BASE_URL,
  appTitle: "HUX Unified",
  endpoints: {},
  userDetails:
    process.env.VUE_APP_OKTA_ISSUER +
    process.env.VUE_APP_OKTA_USER_EDIT_DETAILS,
}
