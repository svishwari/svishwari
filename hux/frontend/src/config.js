export default {
  oidc: {
    clientId: process.env.VUE_APP_OKTA_CLIENT_ID,
    issuer: process.env.VUE_APP_OKTA_ISSUER,
    redirectUri: window.location.origin + "/login/callback",
    scopes: ["openid", "profile", "email"],
    pkce: true,
  },
  apiUrl: process.env.VUE_APP_API_URL || "",
  apiBasePath: "/api/v1",
  oktaUrl: process.env.VUE_APP_OKTA_ISSUER,
  appTitle: "HUX Unified",
  endpoints: {},
  userDetails: `${process.env.VUE_APP_OKTA_ISSUER}/enduser/settings`,
}
