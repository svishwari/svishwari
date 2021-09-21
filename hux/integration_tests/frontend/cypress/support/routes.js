/**
 * URL routes in the application.
 */

export default {
  // auth
  oktaSignInRedirectURI: "/login/callback",
  oktaSignOutRedirectURI: "/login",

  // app
  home: "/",
  login: "/login",
  overview: "/overview",

  // orchestration
  engagements: "/engagements",
  audiences: "/audiences",

  // decisioning
  models: "/models",

  // data Management
  customerProfiles: "/customers",
  identityResolution: "/identity-resolution",
  connections: "/connections",
  destinations: "/destinations",
}
