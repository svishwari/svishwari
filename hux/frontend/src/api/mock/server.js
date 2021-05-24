import { createServer, Factory, Model, Serializer } from "miragejs"
import config from "@/config"

// routes
import { defineRoutes } from "./routes"

// seeds
import seeds from "./seeds"

// factories
import dataSourceFactory from "./factories/dataSource"
import destinationFactory from "./factories/destination"
import engagementFactory from "./factories/engagement"
import audienceFactory from "./factories/audiences"
import modelFactory from "./factories/model"

export function makeServer({ environment = "development" } = {}) {
  // models
  const models = {
    dataSource: Model,
    destination: Model,
    engagement: Model,
    model: Model,
    audience: Model,
  }
  const factories = {
    dataSource: Factory.extend(dataSourceFactory),
    destination: Factory.extend(destinationFactory),
    engagement: Factory.extend(engagementFactory),
    model: Factory.extend(modelFactory),
    audience: Factory.extend(audienceFactory),
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
      application: Serializer.extend({
        embed: true,
        root: false,
      }),
    },
  })

  return server
}
