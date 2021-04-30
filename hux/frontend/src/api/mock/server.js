import { createServer, Model } from "miragejs"
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
      const server = this
      server.namespace = "/api"

      // defineRoutes(server)

      server.get("/destinations", (schema) => {
        return schema.destinations.all().models
      })
    },
  })

  return server
}
