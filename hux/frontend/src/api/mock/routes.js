import { Response } from "miragejs"

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

  // engagements
  server.get("/engagements")
  server.post("/engagements/:id", (schema) => {
    let attrs = this.normalizedRequestAttrs()

    return schema.engagements.create(attrs)
  })

  // models
  server.get("/models")

  // Audiences
  server.get("/audiences")
  server.get("/audiences/:id")
}
