import { belongsTo, createServer, Factory, hasMany, Model } from "miragejs"
import config from "@/config"
import AppSerializer from "./serializer"

// routes
import { defineRoutes } from "./routes"

// seeds
import seeds from "./seeds"

// factories
import { audience as audienceFactory } from "./factories/audiences"
import { customer, customerProfile } from "./factories/customers"
import dataSourceFactory from "./factories/dataSource"
import { destination as destinationFactory } from "./factories/destination"
import { engagement as engagementFactory } from "./factories/engagement"
import { idrDataFeed as idrDataFeedFactory } from "./factories/identity"
import modelFactory from "./factories/model"
import audiencePerformanceFactory from "./factories/audiencePerformance"
import dataExtensionFactory from "./factories/dataExtensions"
import deliveryFactory from "./factories/delivery"
import {
  CampaignMappingOptionsFactory,
  CampaignFactory,
} from "./factories/campaigns"
import { notification as notificationFactory } from "./factories/notifications"

export function makeServer({ environment = "development" } = {}) {
  // models
  const models = {
    audience: Model.extend({
      destinations: hasMany("destination"),
      // engagements: hasMany("engagement"),
    }),
    customer: Model,
    customerProfile: Model,
    dataSource: Model,
    destination: Model.extend({
      destinationable: belongsTo({ polymorphic: true }),
    }),
    idrDataFeed: Model,
    engagement: Model.extend(),
    model: Model,
    audiencePerformance: Model,
    dataExtension: Model,
    deliveryFactory: Model,
    campaign: Model,
    campaignOption: Model,
    notification: Model,
  }

  const factories = {
    audience: Factory.extend(audienceFactory),
    customer: Factory.extend(customer),
    customerProfile: Factory.extend(customerProfile),
    dataSource: Factory.extend(dataSourceFactory),
    destination: Factory.extend(destinationFactory),
    engagement: Factory.extend(engagementFactory),
    idrDataFeed: Factory.extend(idrDataFeedFactory),
    model: Factory.extend(modelFactory),
    audiencePerformance: Factory.extend(audiencePerformanceFactory),
    dataExtension: Factory.extend(dataExtensionFactory),
    delivery: Factory.extend(deliveryFactory),
    campaignOption: Factory.extend(CampaignMappingOptionsFactory),
    campaign: Factory.extend(CampaignFactory),
    notification: Factory.extend(notificationFactory),
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
