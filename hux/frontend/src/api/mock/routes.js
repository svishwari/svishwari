import { Response } from "miragejs"
import { audienceInsights } from "./factories/audiences"
import { customersOverview } from "./factories/customers"
import {
  destinationsConstants,
  destinationsDataExtensions,
} from "./factories/destination"
import idrOverview from "./factories/identity"
import attributeRules from "./factories/attributeRules"

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
  server.get("/destinations/:destinationId/data-extensions")

  server.post("/destinations/validate", (_, request) => {
    const code = 200
    const headers = {}
    const body = { message: "Destination authentication details are valid" }
    const requestData = JSON.parse(request.requestBody)

    if (requestData.type === "salesforce") {
      body.perf_data_extensions = destinationsDataExtensions()
    }
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
      const response = schema.audiencePerformances.find(id)
      return response["email_audience_performance"]
    }
  )
  server.get(
    "/engagements/:id/audience-performance/display-ads",
    (schema, request) => {
      const id = request.params.id
      const response = schema.audiencePerformances.find(id)
      return response["displayads_audience_performance"]
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

  server.post("/customers/overview", () => customersOverview)

  // identity resolution
  server.get("/idr/overview", () => idrOverview)

  // audiences
  server.get("/audiences")

  server.get("/audiences/:id", (schema, request) => {
    const id = request.params.id
    const audience = schema.audiences.find(id)
    return {
      ...audience.attrs,
      audience_insights: audienceInsights,
    }
  })

  server.post("/audiences", (schema, request) => {
    const requestData = JSON.parse(request.requestBody)
    if (requestData.engagements) {
      requestData.engagements = requestData.engagements.map((id) => {
        return schema.engagements.find(id)
      })
    }
    if (requestData.destinations) {
      requestData.destinations = requestData.destinations.map((id) => {
        return schema.destinations.find(id)
      })
    }
    return schema.audiences.create(requestData)
  })

  server.get("/audiences/rules", () => attributeRules)
}
