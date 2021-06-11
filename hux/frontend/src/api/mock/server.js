import { belongsTo, createServer, Factory, hasMany, Model } from "miragejs"
import config from "@/config"
import AppSerializer from "./serializer"

// routes
import { defineRoutes } from "./routes"

// seeds
import seeds from "./seeds"

// factories
import audienceFactory from "./factories/audiences"
import { customer, customerProfile } from "./factories/customers"
import dataSourceFactory from "./factories/dataSource"
import destinationFactory from "./factories/destination"
import engagementFactory from "./factories/engagement"
import modelFactory from "./factories/model"

export function makeServer({ environment = "development" } = {}) {
  // models
  const models = {
    audience: Model.extend({
      destinations: hasMany("destination"),
      engagements: hasMany("engagement"),
    }),
    customer: Model,
    customerProfile: Model,
    dataSource: Model,
    destination: Model.extend({
      destinationable: belongsTo({ polymorphic: true }),
    }),
    engagement: Model.extend(),
    model: Model,
  }

  const factories = {
    audience: Factory.extend(audienceFactory),
    customer: Factory.extend(customer),
    customerProfile: Factory.extend(customerProfile),
    dataSource: Factory.extend(dataSourceFactory),
    destination: Factory.extend(destinationFactory),
    engagement: Factory.extend(engagementFactory),
    model: Factory.extend(modelFactory),
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
        include: ["destinations", "engagements"],
      }),
    },
  })

  return server
}
