import { createServer, Factory, Model, Serializer } from "miragejs"
import config from "@/config"
import { defineRoutes } from "./routes"

//seeds
import seeds from "./seeds"

//factories
import destinationFactory from "./factories/destination"
import engagementFactory from "./factories/engagement"
import dataSourcesFactory from "./factories/dataSources"

export function makeServer({ environment = "development" } = {}) {
  const models = {
    destination: Model,
    engagement: Model,
    dataSource: Model,
  }

  const factories = {
    destination: Factory.extend(destinationFactory),
    engagement: Factory.extend(engagementFactory),
    dataSource: Factory.extend(dataSourcesFactory),
  }

  const server = createServer({
    environment: environment,
    models: models,
    factories: factories,
    seeds: seeds,
    routes() {
      this.urlPrefix = config.apiUrl
      this.namespace = config.apiBasePath
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
