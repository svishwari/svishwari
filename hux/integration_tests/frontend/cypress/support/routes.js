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
  myIssues: "/my-issues",

  // data management
  dataSources: "/data-sources",
  identityResolution: "/identity-resolution",

  // decisioning
  models: "/models",

  // customer insights
  customerProfiles: "/customers",
  segmentPlayground: "/segment-playground",

  // orchestration
  destinations: "/destinations",
  addDestinations: "/destinations/add",
  audiences: "/audiences",
  engagements: "/engagements",
  addEngagement: "/engagements/add",

  // email deliverability
  emailDeliverability: "/email-deliverability",

  // add application
  addApplication: "/application/add",
}
