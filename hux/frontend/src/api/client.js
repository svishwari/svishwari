/**
 * Client for managing the underlying http requests generated for each API
 * resource.
 */

import http from "@/api/httpClient"
import resources from "@/api/resources"

const client = {}

// Common resource endpoints
Object.keys(resources).forEach((resource) => {
  const endpoint = resources[resource]
  client[resource] = {
    all: () => http.get(endpoint),
    create: (data) => http.post(endpoint, data),
    delete: (resourceId) => http.delete(`${endpoint}/${resourceId}`),
    find: (resourceId) => http.get(`${endpoint}/${resourceId}`),
    update: (resourceId, data) => http.put(`${endpoint}/${resourceId}`, data),
    batchUpdate: (data) => http.patch(`${endpoint}`, data),
    constants: () => http.get(`${endpoint}/constants`),
  }
})

// Custom one-off resource endpoints
client["customers"].overview = () => {
  return http.get("/customers/overview")
}

client["destinations"].validate = (data) => {
  return http.post("/destinations/validate", data)
}

client["engagements"].deliver = (resourceId, data) => {
  return http.post(`/engagements/${resourceId}/deliver`, data)
}

client["destinations"].dataExtensions = (resourceId) => {
  return http.get(`/destinations/${resourceId}/data-extensions`)
}
client["destinations"].addDataExtensions = (resourceId, data) => {
  return http.post(`/destinations/${resourceId}/data-extensions`, data)
}

client["engagements"].fetchAudiencePerformance = (resourceId, data) => {
  return http.get(
    `/engagements/${resourceId}/audience-performance/${
      data === "ads" ? "display-ads" : "email"
    }`
  )
}

client["identity"].overview = () => {
  return http.get("/idr/overview")
}
client["audiences"].getRules = () => {
  return http.get("/audiences/rules")
}

client["customers"].getOverview = (data) => {
  return http.post("/customers/overview", data)
}

export default client
