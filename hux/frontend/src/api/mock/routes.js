import { Response } from "miragejs"

export const defineRoutes = (server) => {
  // destinations
  server.get("/destinations", (schema) => {
    return schema.destinations.all().models
  })

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
}
