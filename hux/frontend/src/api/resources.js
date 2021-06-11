/**
 * Mapping of API client resources to endpoint URLs.
 */

export default {
  audiences: "/audiences",
  customers: "/customers",
  dataSources: "/data-sources",
  destinations: "/destinations",
  engagements: "/engagements",
  audiencePerformanceByEmail: "/engagements/:id/audience-performance/email",
  audiencePerformanceByAds: "/engagements/:id/audience-performance/display-ads",
  identity: "/idr",
  models: "/models",
}
