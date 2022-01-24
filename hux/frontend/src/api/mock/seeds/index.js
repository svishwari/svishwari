import audienceSeeds from "./audience"
import dataSourceSeeds from "./dataSource"
import destinationSeeds from "./destination"
import engagementSeeds from "./engagement"
import modelSeeds from "./model"
import userSeeds from "./user"
import geoCountry from "./geoCountry"
import configurationSeeds from "./configuration"

/**
 * Seeds the Mirage.js server with mock data.
 *
 * @param {object} server Mirage server
 */
export default function (server) {
  dataSourceSeeds.forEach((seed) => server.create("dataSource", seed))
  destinationSeeds.forEach((seed) => server.create("destination", seed))
  modelSeeds.forEach((seed) => server.create("model", seed))
  audienceSeeds.forEach((seed) => server.create("audience", seed))
  engagementSeeds.forEach((seed) => server.create("engagement", seed))
  userSeeds.forEach((seed) => server.create("user", seed))
  geoCountry.forEach((seed) => server.create("geoCountry", seed))
  configurationSeeds.forEach((seed) => server.create("configuration", seed))

  server.createList("audience", 10)
  server.createList("engagement", 5)
  server.createList("audiencePerformance", 10)
  server.createList("customer", 5000)
  server.createList("dataExtension", 25)
  server.createList("campaignOption", 1)
  server.createList("notification", 1000)
  server.createList("idrDataFeed", 10)
  server.createList("geoCity", 14659)
  server.createList("geoState", 52)
  server.createList("user", 1)
  server.createList("configuration", 5)
}
