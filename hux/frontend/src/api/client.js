/**
 * Client for managing the underlying http requests generated for each API
 * resource.
 */

import http from "@/api/httpClient"
import resources from "@/api/resources"

const client = {}
/* #region Generic endpoints */
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
/* #endregion */

//#region Customers
// Custom one-off resource endpoints
client["customers"].overview = () => {
  return http.get("/customers/overview")
}

client["customers"].getOverview = (data) => {
  return http.post("/customers/overview", data)
}
//#endregion

//#region Destinations endpoints
client["destinations"].validate = (data) => {
  return http.post("/destinations/validate", data)
}

client["destinations"].dataExtensions = (resourceId) => {
  return http.get(`/destinations/${resourceId}/data-extensions`)
}

client["destinations"].createDataExtension = (resourceId, data) => {
  return http.post(`/destinations/${resourceId}/data-extensions`, data)
}
//#endregion

//#region Engagement custom endpoints
client["engagements"].deliver = (resourceId, data) => {
  return http.post(`/engagements/${resourceId}/deliver`, data)
}

client["engagements"].deliverAudience = ({ resourceId, audienceId }, data) => {
  const endpoint = `/engagements/${resourceId}/audience/${audienceId}/deliver`
  return http.post(endpoint, data)
}

client["engagements"].deliverAudienceDestination = (
  { resourceId, audienceId, destinationId },
  data
) => {
  const endpoint = `/engagements/${resourceId}/audience/${audienceId}/destination/${destinationId}/deliver`
  return http.post(endpoint, data)
}

client["engagements"].deliveries = (resourceId, data) => {
  return http.get(`/engagements/${resourceId}/delivery-history`, data)
}

client["engagements"].fetchAudiencePerformance = (resourceId, data) => {
  return http.get(
    `/engagements/${resourceId}/audience-performance/${
      data === "ads" ? "display-ads" : "email"
    }`
  )
}

client["engagements"].getCampaignMappings = ({
  resourceId,
  audienceId,
  destinationId,
}) => {
  return http.get(
    `/engagements/${resourceId}/audience/${audienceId}/destination/${destinationId}/campaign-mappings`
  )
}
client["engagements"].updateCampaignMapping = (
  { resourceId, audienceId, destinationId },
  data
) => {
  return http.put(
    `/engagements/${resourceId}/audience/${audienceId}/destination/${destinationId}/campaigns`,
    data
  )
}
//#endregion Engagement custom endpoints

//#region Customer Identity endpoint(s)
client["identity"].overview = () => {
  return http.get("/idr/overview")
}
//#endregion

//#region audiences endpoints
client["audiences"].getRules = () => {
  return http.get("/audiences/rules")
}

client["audiences"].deliver = (resourceId, data) => {
  return http.post(`/audiences/${resourceId}/deliver`, data)
}
//#endregion

export default client
