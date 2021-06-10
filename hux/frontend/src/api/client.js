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
    batchUpdate: (data) => http.put(`${endpoint}`, data),
    constants: () => http.get(`${endpoint}/constants`),
  }

  // Custom one-off resource endpoints
  if (resource === "destinations") {
    client[resource].validate = (data) => {
      return http.post("/destinations/validate", data)
    }
  }
  if (resource === "engagements") {
    client[resource].deliver = (resourceId, data) => {
      return http.post(`/engagements/${resourceId}/deliver`, data)
    }
    client[resource].fetchAudiencePerformance = (engagementId, type) => {
      const uri = `/engagements/${engagementId}/audience-performance/${
        type === "ads" ? "display-ads" : "email"
      }`
      return http.get(uri)
    }
  }
})

export default client
