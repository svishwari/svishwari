/**
 * URL routes in the application.
 */

export default {
  // auth
  oktaSignInRedirectURI: "/login/callback",
  oktaSignOutRedirectURI: "/login",

  // app
  index: "/",
  login: "/login",
  home: "/home",
  configuration: "/configuration",
  notifications: "/notifications",

  // data management
  dataSources: "/data-sources",
  identityResolution: "/identity-resolution",

  // decisioning
  models: "/models",

  // customer insights
  customerProfiles: "/customers",
  segmentPlayground: "/audiences/add",

  // orchestration
  destinations: "/destinations",
  addDestinations: "/destinations/add",
  audiences: "/audiences",
  engagements: "/engagements",
  addEngagement: "/engagements/add",
}
