import { Response } from "miragejs"
import { customersOverview } from "./factories/customers"
import { destinationsConstants } from "./factories/destination"
import idrOverview from "./factories/identity"

export const defineRoutes = (server) => {
  // data sources
  server.get("/data-sources")

  server.patch("/data-sources", (schema, request) => {
    const requestData = JSON.parse(request.requestBody)

    return schema.dataSources
      .find(requestData.data_source_ids)
      .update(requestData.body)
  })

  // destinations
  server.get("/destinations")

  server.put("/destinations/:id", (schema, request) => {
    const id = request.params.id

    return schema.destinations.find(id).update({ is_added: true })
  })

  server.post("/destinations/validate", () => {
    const code = 200
    const headers = {}
    const body = { message: "Destination authentication details are valid" }
    return new Response(code, headers, body)
  })

  server.get("/destinations/constants", () => destinationsConstants)

  // engagements
  server.get("/engagements")

  server.post("/engagements", (schema, request) => {
    const requestData = JSON.parse(request.requestBody)

    return schema.engagements.create(requestData)
  })

  server.post("/engagements/:id", (schema) => {
    let attrs = this.normalizedRequestAttrs()

    return schema.engagements.create(attrs)
  })

  server.post("/engagements/:id/deliver", () => {
    const code = 200
    const headers = {}
    const body = { message: "Successfully created delivery jobs" }
    return new Response(code, headers, body)
  })
  // Audience Performances
  server.get(
    "/engagements/:id/audience-performance/email",
    (schema, request) => {
      const id = request.params.id
      return schema.audiencePerformances.find(id)
    }
  )
  server.get(
    "/engagements/:id/audience-performance/display-ads",
    (schema, request) => {
      const id = request.params.id
      return schema.audiencePerformances.find(id)
    }
  )

  // models
  server.get("/models")

  // customers
  server.get("/customers", (schema) => {
    const maxPerRequest = 100
    return {
      customers: schema.customers.all().slice(0, maxPerRequest).models,
      total_customers: 827438924,
    }
  })
  server.get("/customers/:id", (schema, request) => {
    const id = request.params.id
    return server.create("customerProfile", schema.customers.find(id).attrs)
  })
  server.get("/customers/overview", () => customersOverview)

  // identity resolution
  server.get("/idr/overview", () => idrOverview)

  // Audiences
  server.get("/audiences")
  server.get("/audiences/:id")
  server.post("/audiences", (schema, request) => {
    const requestData = JSON.parse(request.requestBody)
    return schema.audiences.create(requestData)
  })
}
