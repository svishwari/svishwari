import { Response } from "miragejs"
import { customersOverview } from "./factories/customers"
import idrOverview from "./factories/identity"

export const defineRoutes = (server) => {
  // data sources
  server.get("/data-sources")

  server.put("/data-sources", (schema, request) => {
    const requestData = JSON.parse(request.requestBody)

    return schema.dataSources.find(requestData).update({ is_added: true })
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

  server.get("/destinations/constants", () => {
    const code = 200
    const headers = {}
    const body = {
      facebook: {
        facebook_ad_account_id: {
          name: "Ad Account ID",
          type: "text",
          required: true,
          description: "Placeholder information text for 'Ad Account ID'",
        },
        facebook_app_id: {
          name: "App ID",
          type: "text",
          required: true,
          description: "Placeholder information text for 'App ID'",
        },
        facebook_access_token: {
          name: "Access Token",
          type: "password",
          required: true,
          description: "Placeholder information text for 'Access Token'",
        },
        facebook_app_secret: {
          name: "App Secret",
          type: "password",
          required: true,
          description: "Placeholder information text for 'App Secret'",
        },
      },
      salesforce: {
        sfmc_account_id: {
          name: "Account ID",
          type: "text",
          required: true,
          description: "Placeholder information text for 'Account ID'",
        },
        sfmc_auth_base_uri: {
          name: "Auth Base URI",
          type: "text",
          required: true,
          description: "Placeholder information text for 'Auth Base URI'",
        },
        sfmc_client_id: {
          name: "Client ID",
          type: "text",
          required: true,
          description: "Placeholder information text for 'Client ID'",
        },
        sfmc_client_secret: {
          name: "Client Secret",
          type: "password",
          required: true,
          description: "Placeholder information text for 'Client Secret'",
        },
        sfmc_rest_base_uri: {
          name: "REST Base URI",
          type: "text",
          required: true,
          description: "Placeholder information text for 'REST Base URI'",
        },
        sfmc_soap_base_uri: {
          name: "Soap Base URI",
          type: "text",
          required: true,
          description: null,
        },
      },
    }
    return new Response(code, headers, body)
  })

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
