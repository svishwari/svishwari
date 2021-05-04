import { createServer, Model } from "miragejs"
import config from "@/config"
import { defineRoutes } from "./routes"
import seeds from "./seeds"
import destinationFactory from "./factories/destination"

const models = {
  destination: Model,
}

const factories = {
  destination: destinationFactory,
}

export function makeServer({ environment = "development" } = {}) {
  let server = createServer({
    environment,

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
  })

  return server
}
