/**
 * Client for managing the underlying http requests generated for each API
 * resource.
 */

import http from "@/api/httpClient"
import resources from "@/api/resources"

const client = {}

Object.keys(resources).forEach((resource) => {
  const endpoint = resources[resource]

  // Common resource endpoints
  client[resource] = {
    all: () => http.get(endpoint),
    create: (data) => http.post(endpoint, data),
    delete: (resourceId) => http.delete(`${endpoint}/${resourceId}`),
    find: (resourceId) => http.get(`${endpoint}/${resourceId}`),
    update: (resourceId, data) => http.put(`${endpoint}/${resourceId}`, data),
  }

  // Custom one-off endpoints
  if (resource === "destinations") {
    client[resource].validate = (data) => {
      http.post("/destinations/validate", data)
    }
  }
})

export default client
