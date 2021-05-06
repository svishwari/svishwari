import { Response } from "miragejs"

export const defineRoutes = (server) => {
  // destinations
  server.get("/destinations", (schema) => {
    return schema.destinations.all().models
  })

  server.put("/destinations/:id")

  server.post("/destinations/validate", () => {
    const code = 200
    const headers = {}
    const body = { message: "Destination authentication details are valid" }

    return new Response(code, headers, body)
  })
}
