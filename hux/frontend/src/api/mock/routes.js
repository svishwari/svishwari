export const defineRoutes = (server) => {
  server.get("/destinations", (schema) => {
    return schema.destinations.all().models
  })
}
