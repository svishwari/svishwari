import { Response } from "miragejs"

export const defineRoutes = (server) => {
  // destinations
  server.get("/destinations")

  server.put("/destinations/:id", (schema, request) => {
    const id = request.params.id

    // here we assume if we added the destination and its validated
    // the destination is successfully updated

    return schema.destinations.find(id).update({ is_added: true })
  })

  server.post("/destinations/validate", () => {
    const code = 200
    const headers = {}
    const body = { message: "Destination authentication details are valid" }

    return new Response(code, headers, body)
  })

  // data sources
  server.get("/data-sources")

  server.put("/data-sources", (schema, request) => {
    const requestData = JSON.parse(request.requestBody)

    return schema.dataSources.find(requestData).update({ is_added: true })
  })
}
