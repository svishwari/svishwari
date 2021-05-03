import { createServer, Model } from "miragejs"

import config from "@/config"

// import { defineRoutes } from "./resources"

export function makeServer({ environment = "development" } = {}) {
  let server = createServer({
    environment,

    models: {
      destination: Model,
    },

    seeds(server) {
      server.create("destination", {
        id: 1,
        title: "Facebook",
        type: "facebook",
      })
      server.create("destination", {
        id: 2,
        title: "Salesforce Marketing",
        type: "salesforce",
      })
      server.create("destination", { id: 3, title: "Twillio", type: "twillio" })
    },

    routes() {
      this.urlPrefix = config.apiUrl
      this.namespace = "/api/v1"

      // defineRoutes(this)

      this.get("/destinations", (schema) => {
        return schema.destinations.all().models
      })

      // pass requests to external APIs through
      this.passthrough(`${config.oktaUrl}/**`)
    },
  })

  return server
}
