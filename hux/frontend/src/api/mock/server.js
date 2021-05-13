import { createServer, Factory, Model, Serializer } from "miragejs"
import config from "@/config"
import { defineRoutes } from "./routes"
import seeds from "./seeds"
import destinationFactory from "./factories/destination"
import engagementFactory from "./factories/engagement"

export function makeServer({ environment = "development" } = {}) {
  const models = {
    destination: Model,
    engagement: Model,
  }

  const factories = {
    destination: Factory.extend(destinationFactory),
    engagement: Factory.extend(engagementFactory),
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
