/**
 * Mock API server using Mirage.js - only included in src/main.js for local
 * development and for unit testing and not for production builds.
 */
import { belongsTo, createServer, Factory, hasMany, Model } from "miragejs"
import config from "@/config"
import AppSerializer from "./serializer"

// routes
import { defineRoutes } from "./routes"

// seeds
import seeds from "./seeds/index"

// factories
import { audience as audienceFactory } from "./factories/audiences"
import {
  customer,
  customerProfile,
  geoCity,
  geoCountry,
  geoState,
} from "./factories/customers"
import dataSourceFactory from "./factories/dataSource"
import { destination as destinationFactory } from "./factories/destination"
import { engagement as engagementFactory } from "./factories/engagement"
import { idrDataFeed as idrDataFeedFactory } from "./factories/identity"
import modelFactory from "./factories/model"
import audiencePerformanceFactory from "./factories/audiencePerformance"
import dataExtensionFactory from "./factories/dataExtensions"
import deliveryFactory from "./factories/delivery"
import { configuration as configurationFactory } from "./factories/configuration"
import {
  CampaignMappingOptionsFactory,
  CampaignFactory,
} from "./factories/campaigns"
import { notification as notificationFactory } from "./factories/notifications"
import { user as userFactory } from "./factories/user"

/**
 * Starts up a Mirage server with the given configuration.
 *
 * @param {object} config mirage server configuration
 * @param {string} config.environment environment server is running in
 * @returns {object} mirage server
 */
export function makeServer({ environment = "development" } = {}) {
  // models
  const models = {
    audience: Model.extend({
      destinations: hasMany("destination"),
      // engagements: hasMany("engagement"),
    }),
    audiencePerformance: Model,
    customer: Model,
    customerProfile: Model,
    dataSource: Model,
    destination: Model.extend({
      destinationable: belongsTo({ polymorphic: true }),
    }),
    campaign: Model,
    campaignOption: Model,
    dataExtension: Model,
    deliveryFactory: Model,
    engagement: Model.extend(),
    geoCity: Model,
    geoCountry: Model,
    geoState: Model,
    idrDataFeed: Model,
    model: Model,
    notification: Model,
    user: Model,
    configuration: Model,
  }

  const factories = {
    audience: Factory.extend(audienceFactory),
    audiencePerformance: Factory.extend(audiencePerformanceFactory),
    campaign: Factory.extend(CampaignFactory),
    campaignOption: Factory.extend(CampaignMappingOptionsFactory),
    customer: Factory.extend(customer),
    customerProfile: Factory.extend(customerProfile),
    dataExtension: Factory.extend(dataExtensionFactory),
    dataSource: Factory.extend(dataSourceFactory),
    delivery: Factory.extend(deliveryFactory),
    destination: Factory.extend(destinationFactory),
    engagement: Factory.extend(engagementFactory),
    geoCity: Factory.extend(geoCity),
    geoCountry: Factory.extend(geoCountry),
    geoState: Factory.extend(geoState),
    idrDataFeed: Factory.extend(idrDataFeedFactory),
    model: Factory.extend(modelFactory),
    notification: Factory.extend(notificationFactory),
    user: Factory.extend(userFactory),
    configuration: Factory.extend(configurationFactory),
  }

  const server = createServer({
    environment: environment,
    models: models,
    factories: factories,
    seeds: seeds,
    routes() {
      this.urlPrefix = config.apiUrl
      this.namespace = config.apiBasePath
      this.timing = 1000
      defineRoutes(this)

      // whenever we connect from local to the dev API we will need to override
      // the access token with one provided by dev in token.txt
      if (environment === "development" && config.apiUrl.includes("dev1.in")) {
        this.passthrough((request) => {
          if (request.url.includes("dev1.in")) {
            const TOKEN_OVERRIDE = require("./token.txt")["default"]
            request.requestHeaders["Authorization"] = `Bearer ${TOKEN_OVERRIDE}`
          }
          return request
        })
      }

      // pass requests to external APIs through
      this.passthrough(`${config.oktaUrl}/**`)
    },
    serializers: {
      application: AppSerializer,
      audience: AppSerializer.extend({
        include: [
          "destinations",
          // "engagements"
        ],
      }),
      customer: AppSerializer.extend({
        root: true,
      }),
    },
  })

  return server
}
