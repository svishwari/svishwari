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
  server.get("/destinations/:id")

  server.put("/destinations/:id", (schema, request) => {
    const id = request.params.id

    return schema.destinations.find(id).update({ is_added: true })
  })
  server.get("/destinations/:destinationId/data-extensions")
  server.post(
    "/destinations/:destinationId/data-extensions",
    (schema, request) => {
      const requestData = JSON.parse(request.requestBody)
      const requestPayload = {
        name: requestData.data_extension,
      }
      let response = schema.dataExtensions.create(requestPayload)
      // update data extension, assign the new `id` to its `data_extension_id`
      let updatedResponse = schema.dataExtensions
        .find(response.attrs.id)
        .update({ data_extension_id: response.attrs.id })
      return updatedResponse.attrs
    }
  )

  server.post("/destinations/validate", (_, request) => {
    const code = 200
    const headers = {}
    const body = { message: "Destination authentication details are valid" }
    const requestData = JSON.parse(request.requestBody)

    if (requestData.type === "sfmc") {
      body.perf_data_extensions = destinationsDataExtensions()
    }
    return new Response(code, headers, body)
  })

  server.get("/destinations/constants", () => destinationsConstants)

  // engagements
  server.get("/engagements")

  server.get("/engagements/:id", (schema, request) => {
    const id = request.params.id
    const engagement = schema.engagements.find(id)
    return engagement
  })

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

  // Attaching an Audience to an Engagement
  server.post("/engagements/:id/audiences", (schema, request) => {
    const code = 200
    const headers = {}
    const id = request.params.id
    const requestData = JSON.parse(request.requestBody)
    const engagement = schema.engagements.find(id)
    const addedAudiences = requestData.audiences.map((aud) => {
      const audience = schema.audiences.find(aud.id)
      const existsAudience = engagement.audiences.filter(
        (engAud) => engAud.id === aud.id
      )
      if (existsAudience.length > 0) {
        existsAudience[0].destinations = aud.destinations
        return
      }
      const audienceObj = {
        status: audience.status,
        id: audience.id,
        name: audience.name,
        destinations: aud.destinations.map((des) =>
          schema.destinations.find(des.id)
        ),
      }
      return audienceObj
    })
    if (!addedAudiences.includes(undefined)) {
      engagement.audiences.push(...addedAudiences)
    }
    const body = { message: "SUCCESS" }
    return new Response(code, headers, body)
  })

  // Detaching an Audience to an Engagement
  server.del("/engagements/:id/audiences/:audienceId", (schema, request) => {
    const code = 200
    const headers = {}
    const id = request.params.id
    const audienceId = request.params.audienceId
    const engagement = schema.engagements.find(id)
    engagement.audiences.splice(
      engagement.audiences.findIndex((aud) => aud.id === audienceId),
      1
    )
    const body = { message: "SUCCESS" }
    return new Response(code, headers, body)
  })

  server.post("/engagements/:id/audience/:audienceId/deliver", () => {
    return { message: "Successfully created delivery jobs" }
  })

  server.post(
    "/engagements/:id/audience/:audienceId/destination/:destinationId/deliver",
    () => {
      return { message: "Successfully created delivery jobs" }
    }
  )
  server.get(
    "/engagements/:id/audience/:audienceId/destination/:destinationId/campaign-mappings",
    (schema) => {
      return schema.campaigns.all()
    }
  )
  server.put(
    "/engagements/:id/audience/:audienceId/destination/:destinationId/campaigns",
    () => {
      return { message: "Successfully created mappings" }
    }
  )

  server.get("/engagements/:id/delivery-history", (schema, request) => {
    const id = request.params.id
    const engagement = schema.engagements.find(id)
    const destination = schema.destinations.find(7)
    return engagement.audiences.map((audience) => {
      return {
        audience: {
          id: audience.id,
          name: audience.name,
        },
        destination: {
          id: destination.id,
          name: destination.name,
          type: destination.type,
        },
        size: audience.size,
        delivered: "2021-07-11T14:39:49.574Z",
      }
    })
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
  server.get("/customers")

  server.get("/customers/:id", (schema, request) => {
    const id = request.params.id
    return server.create("customerProfile", schema.customers.find(id).attrs)
  })

  server.get("/customers/overview", () => customersOverview)

  server.post("/customers/overview", () => customersOverview)

  // identity resolution
  server.get("/idr/overview", () => idrOverview)

  // notification
  server.get("/notifications")

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

  server.post("/audiences/:id/deliver", () => {
    return { message: "Successfully created delivery jobs" }
  })

  server.get("/audiences/rules", () => attributeRules)
}
