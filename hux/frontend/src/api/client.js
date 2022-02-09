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

//#region Users
client["users"].fetchProfile = () => {
  return http.get("/users/profile")
}
client["users"].updatePreferences = (data) => {
  return http.put("/users/preferences", data)
}
client["users"].markFavorite = (resourceId, entityType) => {
  return http.post(`users/${entityType}/${resourceId}/favorite`)
}
client["users"].clearFavorite = (resourceId, entityType) => {
  return http.delete(`users/${entityType}/${resourceId}/favorite`)
}
client["users"].contactUs = (data) => {
  return http.post("users/contact-us", data)
}
client["users"].requestTeamMember = (data) => {
  return http.post("users/request_new_user", data)
}
client["users"].getRequestedUsers = () => {
  return http.get("users/requested_users")
}
client["users"].tickets = () => {
  return http.get("users/tickets")
}
//#endregion

//#region Customers
// Custom one-off resource endpoints

client["customers"].getRedact = (id, redactFlag) => {
  return http.get(`/customers/${id}?redact=${redactFlag}`)
}

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

client["customers"].getCustomerSpend = () => {
  return http.get("/customers-insights/revenue")
}

client["customers"].events = (huxId) => {
  const emptyDateFilter = {}
  return http.post(`/customers/${huxId}/events`, emptyDateFilter)
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

client["destinations"].request = (data) => {
  return http.post("/destinations/request", data)
}

client["destinations"].authenticate = (destinationId, data) => {
  return http.put(`/destinations/${destinationId}/authentication`, data)
}

client["destinations"].remove = (id, data) => {
  return http.patch(`/destinations/${id}`, data)
}

client["destinations"].dataExtensions = (resourceId) => {
  return http.get(`/destinations/${resourceId}/data-extensions`)
}

client["destinations"].createDataExtension = (resourceId, data) => {
  return http.post(`/destinations/${resourceId}/data-extensions`, data)
}
//#endregion

//#region Engagement custom endpoints
client["engagements"].allFiltered = (data) => {
  let URLData = []
  for (const property in data) {
    let formURL = property + "=" + data[property]
    URLData.push(formURL)
  }
  let newURLFormat = URLData.join("@").toString().replace(/@/g, "&")
  return http.get(`/engagements?${newURLFormat}`)
}

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

client["engagements"].deliverySchedule = ({
  id,
  audienceId,
  destinationId,
  recurringConfig,
}) => {
  const endpoint = `/engagements/${id}/audience/${audienceId}/destination/${destinationId}/schedule`
  return http.post(endpoint, recurringConfig)
}

client["engagements"].deliverAudienceDestination = (
  { resourceId, audienceId, destinationId },
  data
) => {
  const endpoint = `/engagements/${resourceId}/audience/${audienceId}/destination/${destinationId}/deliver`
  return http.post(endpoint, data)
}

client["engagements"].deliveries = (resourceId, query) => {
  return http.get(`/engagements/${resourceId}/delivery-history?${query}`)
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

client["engagements"].remove = (resourceId) => {
  return http.delete(`/engagements/${resourceId}`)
}
//#endregion Engagement custom endpoints

//#region Customer Identity endpoint(s)
client["idr"].overview = (params) => {
  return http.get("/idr/overview", { timeout: 0, params: params })
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

client["audiences"].getrulesByFields = (params) => {
  return http.get(`/audiences/rules/${params.fieldType}/${params.key}`)
}

client["audiences"].createAndDeliver = (data) => {
  return http.post("/audiences?deliver=true", data)
}

client["audiences"].getAudiences = (data) => {
  let URLData = []
  let newURLFormat
  let URLString
  for (const property in data) {
    if (property == "attribute") {
      for (const attribute in data[property]) {
        let formURL = property + "=" + data[property][attribute]
        URLData.push(formURL)
      }
    } else {
      let formURL = property + "=" + data[property]
      URLData.push(formURL)
    }
  }
  let arrJoin = URLData.join("@")
  URLString = arrJoin.toString()
  newURLFormat = URLString.replace(/@/g, "&")
  return http.get(`/audiences?${newURLFormat}`)
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

client["audiences"].deliveries = (resourceId, query) => {
  return http.get(`/audiences/${resourceId}/delivery-history?${query}`)
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

client["audiences"].remove = (resourceId) => {
  return http.delete(`/audiences/${resourceId}`)
}

client["audiences"].removeStandaloneDestination = (resourceId, data) => {
  return http.delete(`audiences/${resourceId}/destinations`, { data: data })
}

client["audiences"].histogram = (field, model) => {
  let url = `/audiences/rules/${field}/histogram`
  if (model) {
    url = url + `?model_name=${model}`
  }
  return http.get(url)
}
//#endregion

//#region Notifications
client["notifications"].getNotifications = (data) => {
  delete data.isLazyLoad
  let URLData = []
  let newURLFormat
  let URLString
  for (const property in data) {
    let formURL = property + "=" + data[property]
    URLData.push(formURL)
  }
  let arrJoin = URLData.join("@")
  URLString = arrJoin.toString()
  newURLFormat = URLString.replace(/@/g, "&")
  return http.get(`/notifications?${newURLFormat}`)
}

client["notifications"].find = (notification_id) => {
  return http.get(`/notifications/${notification_id}`)
}

client["notifications"].getAllUsers = () => {
  return http.get("/users")
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

client["models"].remove = (model) => {
  return http.delete(`/models?model_id=${model.id}`)
}

//#region Data sources
client.dataSources.dataFeeds = (type) => {
  return http.get(`/data-sources/${type}/datafeeds`)
}
client.dataSources.dataFeedsDetails = (type, name) => {
  return http.get(`/data-sources/${type}/datafeeds/${name}`)
}
//#endregion

//#region Application
client.applications.getActiveApplications = (flag) => {
  return http.get(`/applications?only_active=${flag}`)
}

client.applications.createApplication = (data) => {
  return http.post("/applications", data)
}

client.applications.updateApplication = (id, data) => {
  return http.patch(`/applications/${id}`, data)
}

export default client
