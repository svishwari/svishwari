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

client["customers"].geoOverview = () => http.get("/customers-insights/geo")

client["customers"].geoCities = (batchNumber, batchSize) => {
  return http.get(
    `/customers-insights/cities?batch_number=${batchNumber}&batch_size=${batchSize}`
  )
}

client["customers"].geoCountries = () => {
  return http.get("/customers-insights/countries")
}

client["customers"].geoStates = () => {
  return http.get("/customers-insights/states")
}

client["customers"].demographics = (data) => {
  return http.get(
    `/customers-insights/demo?start_date=${data.start_date}&end_date=${data.end_date}`
  )
}

client["customers"].totalCustomers = () => {
  return http.get("/customers-insights/total")
}

client["customers"].events = (huxId) => {
  return http.post(`/customers/${huxId}/events`)
}

client["customers"].getOverview = (data) => {
  return http.post("/customers/overview", data)
}

client["customers"].getCustomers = (batchSize, batchNumber) => {
  return http.get(
    `/customers?batch_size=${batchSize}&batch_number=${batchNumber}`
  )
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

client["engagements"].attachAudience = (resourceId, data) => {
  return http.post(`/engagements/${resourceId}/audiences`, data)
}
client["engagements"].attachDestination = (engagementId, audienceId, data) => {
  return http.post(
    `/engagements/${engagementId}/audience/${audienceId}/destinations`,
    data
  )
}

client["engagements"].detachDestination = (engagementId, audienceId, data) => {
  // NOTE: The Hux API supports post data for a DELETE request method.
  // Typically, this isn't RESTful so Mirage does not support this, hence this check
  if (process.env.NODE_ENV !== "development") {
    return http.delete(
      `/engagements/${engagementId}/audience/${audienceId}/destinations`,
      { data: data }
    )
  } else {
    return http.delete(
      `/engagements/${engagementId}/audience/${audienceId}/destinations/${data.id}`
    )
  }
}

client["engagements"].detachAudience = (resourceId, data) => {
  // NOTE: The Hux API supports post data for a DELETE request method.
  // Typically, this isn't RESTful so Mirage does not support this, hence this check
  if (process.env.NODE_ENV !== "development") {
    return http.delete(`/engagements/${resourceId}/audiences`, { data: data })
  } else {
    const audienceId = data.audience_ids[0]
    return http.delete(`/engagements/${resourceId}/audiences/${audienceId}`)
  }
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

client["engagements"].getCampaignMappingOptions = ({
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

client["engagements"].downloadAudienceMetrics = (engagementId) => {
  return http.get(
    `/engagements/${engagementId}/audience-performance/download`,
    {
      timeout: 0,
      responseType: "blob",
    }
  )
}

client["engagements"].getCampaigns = ({
  resourceId,
  audienceId,
  destinationId,
}) => {
  return http.get(
    `/engagements/${resourceId}/audience/${audienceId}/destination/${destinationId}/campaigns`
  )
}
//#endregion Engagement custom endpoints

//#region Customer Identity endpoint(s)
client["idr"].overview = (params) => {
  return http.get("/idr/overview", { params: params })
}

client["idr"].datafeeds = (params) => {
  return http.get("/idr/datafeeds", { params: params })
}

client["idr"].datafeedReport = (id) => {
  return http.get(`/idr/datafeeds/${id}`)
}

client["idr"].matchingTrends = (params) => {
  return http.get("/idr/matching-trends", { params: params })
}
//#endregion

//#region audiences endpoints
client["audiences"].getRules = () => {
  return http.get("/audiences/rules")
}

client["audiences"].downloadAudience = (audienceId, fileType) => {
  return http.get(`/audiences/${audienceId}/${fileType}`, {
    timeout: 0,
    responseType: "blob",
  })
}

client["audiences"].demographics = (audienceId) => {
  return http.get(`/audiences/${audienceId}/audience_insights`)
}

client["audiences"].deliver = (resourceId, data) => {
  return http.post(`/audiences/${resourceId}/deliver`, data)
}

client["audiences"].deliveries = (resourceId, data) => {
  return http.get(`/audiences/${resourceId}/delivery-history`, data)
}

client["audiences"].geoCities = (resourceId, batchNumber, batchSize) => {
  return http.get(
    `/audiences/${resourceId}/cities?batch_number=${batchNumber}&batch_size=${batchSize}`
  )
}

client["audiences"].geoCountries = (resourceId) => {
  return http.get(`/audiences/${resourceId}/countries`)
}

client["audiences"].geoStates = (resourceId) => {
  return http.get(`/audiences/${resourceId}/states`)
}
//#endregion

//#region Notifications
client["notifications"].getNotifications = (batchSize, batchNumber) => {
  return http.get(
    `/notifications?batch_size=${batchSize}&batch_number=${batchNumber}`
  )
}
//#endregion

client["models"].overview = (id) => {
  return http.get(`/models/${id}/overview`)
}

client["models"].features = (id) => {
  return http.get(`/models/${id}/feature-importance`)
}

client["models"].versionHistory = (id) => {
  return http.get(`/models/${id}/version-history`)
}

client["models"].lift = (id) => {
  return http.get(`/models/${id}/lift`)
}

client["models"].drift = (id) => {
  return http.get(`/models/${id}/drift`)
}

client["models"].modelFeatures = (id) => {
  return http.get(`/models/${id}/features`)
}

//#region Data sources
client.dataSources.dataFeeds = (type) => {
  return http.get(`/data-sources/${type}/datafeeds`)
}
//#endregion

export default client
