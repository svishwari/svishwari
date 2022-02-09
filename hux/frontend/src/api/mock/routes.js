import { Response } from "miragejs"
import dayjs from "dayjs"
import faker from "faker"

import { audienceInsights } from "./factories/audiences"
import { customersOverview } from "./factories/customers"
import { me } from "./factories/me"
import {
  destinationsConstants,
  destinationsDataExtensions,
} from "./factories/destination"
import { idrOverview, idrDataFeedReport } from "./factories/identity"
import { dataFeeds, dataFeedDetails } from "./factories/dataSource"
import attributeRules from "./factories/attributeRules"
import featureData from "./factories/featureData.json"
import { requestedUser, someTickets } from "./factories/user.js"
import audienceCSVData from "./factories/audienceCSVData"
import liftData from "./factories/liftChartData"
import mapData from "@/components/common/MapChart/mapData.js"
import demographicsData from "@/api/mock/fixtures/demographicData.js"
import customerEventData from "@/api/mock/fixtures/customerEventData.js"
import totalCustomersData from "./fixtures/totalCustomersData.js"
import totalCustomerSpendData from "./fixtures/totalCustomerSpendData.js"
import { driftData } from "@/api/mock/factories/driftData.js"
import idrMatchingTrends from "@/api/mock/fixtures/idrMatchingTrendData.js"
import { applications } from "./factories/application"

export const defineRoutes = (server) => {
  // Users
  server.get("/users/profile", (schema) => {
    return schema.users.find(1)
  })
  server.post("users/:type/:id/favorite", (schema, request) => {
    const code = 200
    const headers = {}
    const body = { message: "SUCCESS" }
    const id = request.params.id
    const favoriteType = request.params.type
    const user = schema.users.find(1)

    user.favorites[favoriteType].push(id)
    return new Response(code, headers, body)
  })
  server.del("users/:type/:id/favorite", (schema, request) => {
    const code = 200
    const headers = {}
    const body = { message: "SUCCESS" }
    const id = request.params.id
    const favoriteType = request.params.type
    const user = schema.users.find(1)

    user.favorites[favoriteType] = user.favorites[favoriteType].filter(
      (item) => item !== id
    )
    return new Response(code, headers, body)
  })
  server.post("users/contact-us", () => {
    const code = 201
    const headers = {}
    const body = {
      description: "test summary",
      id: 116331,
      key: "HUS-1553",
      summary: "test",
    }
    return new Response(code, headers, body)
  })
  server.post("users/request_new_user", (_, request) => {
    const code = 201
    const headers = {}
    const requestData = JSON.parse(request.requestBody)
    const body = {
      description:
        "*Project Name:* ADV \n*Required Info:* Please add them to the team-unified--base group. \n*Reason for Request:* New member to our team \n*User:* " +
        requestData.first_name +
        "\n*Email:*" +
        requestData.email +
        "\n*Access Level:* admin \n*PII Access:*" +
        requestData.pii_access +
        " \n*Okta Group Name:* team-unified--base \n*Okta App:* HUX Audience Builder \n*Requested by:*" +
        me.full_name(),
      key: "HUS-" + `${faker.datatype.number({ min: 1000, max: 3000 })}`,
      id: faker.datatype.number({ min: 100000, max: 1000000 }),
      summary: "[NEW USER REQUEST] for " + requestData.email,
    }
    return new Response(code, headers, body)
  })
  server.get("users/requested_users", () => requestedUser)
  server.get("users/tickets", () => someTickets())

  //client projects
  server.get("/client-projects")

  // data sources
  server.get("/data-sources")

  server.get("/data-sources/:id")

  server.get("/data-sources/:type/datafeeds", (schema, request) => {
    const dataSourceType = request.params["type"]
    const dataSource = schema.dataSources.findBy({ type: dataSourceType }).attrs
    return dataFeeds(dataSource)
  })

  server.get("/data-sources/:type/datafeeds/:name", (schema, request) => {
    const dataSourceType = request.params["type"]
    const dataSourceFeedName = request.params["name"]
    return dataFeedDetails(dataSourceType, dataSourceFeedName)
  })

  server.patch("/data-sources", (schema, request) => {
    const requestData = JSON.parse(request.requestBody)

    return schema.dataSources
      .find(requestData.data_source_ids)
      .update(requestData.body)
  })

  // destinations
  server.get("/destinations")
  server.get("/destinations/:id")

  server.put("/destinations/:id/authentication", (schema, request) => {
    const id = request.params.id
    const requestData = JSON.parse(request.requestBody)

    return schema.destinations.find(id).update({
      is_added: true,
      status: "Active",
      configuration: requestData.configuration,
    })
  })

  server.patch("/destinations/:id", (schema, request) => {
    const id = request.params.id

    return schema.destinations
      .find(id)
      .update({ is_added: false, status: "Pending" })
  })

  server.get("/destinations/:destinationId/data-extensions")
  server.post(
    "/destinations/:destinationId/data-extensions",
    (schema, request) => {
      const requestData = JSON.parse(request.requestBody)
      const requestPayload = {
        name: requestData.data_extension,
      }
      let response = schema.dataExtensions.create(requestPayload)
      // update data extension, assign the new `id` to its `data_extension_id`
      let updatedResponse = schema.dataExtensions
        .find(response.attrs.id)
        .update({
          data_extension_id: response.attrs.id,
          create_time: new Date(),
        })
      return updatedResponse.attrs
    }
  )

  server.post("/destinations/validate", (_, request) => {
    const code = 200
    const headers = {}
    const body = { message: "Destination authentication details are valid" }
    const requestData = JSON.parse(request.requestBody)

    if (requestData.type === "sfmc") {
      body.perf_data_extensions = destinationsDataExtensions()
    }
    return new Response(code, headers, body)
  })

  server.post("/destinations/request", (schema, request) => {
    const requestDetails = JSON.parse(request.requestBody)
    const { name } = requestDetails
    const existingDestination = schema.destinations.findBy({ name: name })
    if (existingDestination) {
      return existingDestination.update({ is_added: true, status: "Requested" })
    } else {
      const attrs = {
        ...requestDetails,
        type: "generic_destination",
        category: "Other",
        status: "Requested",
        is_added: true,
      }
      return server.create("destination", attrs)
    }
  })

  server.get("/destinations/constants", () => destinationsConstants)

  // engagements
  server.get("/engagements")

  server.get("/engagements/:id", (schema, request) => {
    const id = request.params.id
    const engagement = schema.engagements.find(id)
    return engagement
  })

  server.post("/engagements", (schema, request) => {
    const requestData = JSON.parse(request.requestBody)

    let errorResponse

    // validations: duplicate name
    let duplicateLength = schema.engagements.where({
      name: requestData.name,
    }).models.length

    if (duplicateLength > 0) {
      errorResponse = {
        message: "Name already exists.",
      }
    }

    // validations: null as description
    if (requestData.description === null) {
      errorResponse = {
        description: ["Field may not be null."],
      }
    }

    if (errorResponse) {
      const errorCode = 400
      const errorHeaders = {}
      return new Response(errorCode, errorHeaders, errorResponse)
    }

    const now = dayjs().toJSON()

    const attrs = {
      ...requestData,
      create_time: () => now,
      created_by: me.full_name(),
      update_time: () => now,
      updated_by: me.full_name(),
    }

    return server.create("engagement", attrs)
  })

  server.post("/engagements/:id", (schema) => {
    let attrs = this.normalizedRequestAttrs()

    return schema.engagements.create(attrs)
  })

  server.post("/engagements/:id/deliver", () => {
    const code = 200
    const headers = {}
    const body = { message: "Successfully created delivery jobs" }
    return new Response(code, headers, body)
  })

  // Attaching an Audience to an Engagement
  server.post("/engagements/:id/audiences", (schema, request) => {
    const code = 200
    const headers = {}
    const id = request.params.id
    const requestData = JSON.parse(request.requestBody)
    const engagement = schema.engagements.find(id)
    const addedAudiences = requestData.audiences.map((aud) => {
      const audience = schema.audiences.find(aud.id)
      const existsAudience = engagement.audiences.filter(
        (engAud) => engAud.id === aud.id
      )
      if (existsAudience.length > 0) {
        existsAudience[0].destinations = aud.destinations.map((des) =>
          schema.destinations.find(des.id)
        )
        return
      }
      const audienceObj = {
        status: audience.status,
        id: audience.id,
        name: audience.name,
        destinations: aud.destinations.map((des) =>
          schema.destinations.find(des.id)
        ),
      }
      return audienceObj
    })
    if (!addedAudiences.includes(undefined)) {
      engagement.audiences.push(...addedAudiences)
    }
    const body = { message: "SUCCESS" }
    return new Response(code, headers, body)
  })

  // Detaching an Audience to an Engagement
  server.del("/engagements/:id/audiences/:audienceId", (schema, request) => {
    const code = 200
    const headers = {}
    const id = request.params.id
    const audienceId = request.params.audienceId
    const engagement = schema.engagements.find(id)
    engagement.audiences.splice(
      engagement.audiences.findIndex((aud) => aud.id === audienceId),
      1
    )
    const body = { message: "SUCCESS" }
    return new Response(code, headers, body)
  })

  // Detaching a destination from an Engagement
  server.del(
    "/engagements/:id/audience/:audienceId/destinations/:destinationId",
    (schema, request) => {
      const code = 200
      const headers = {}
      const id = request.params.id
      const destinationId = request.params.destinationId
      const engagement = schema.engagements.find(id)
      Object.values(engagement.destinations_category).forEach((category) => {
        for (
          var index = category.destinations.length - 1;
          index >= 0;
          --index
        ) {
          if (category.destinations[index].id == destinationId) {
            category.destinations.splice(index, 1)
          }
        }
      })
      const body = { message: "SUCCESS" }
      return new Response(code, headers, body)
    }
  )

  server.post(
    "/engagements/:id/audience/:audienceId/deliver",
    (schema, request) => {
      const engagementId = request.params.id
      const audienceId = request.params.audienceId

      const engagement = schema.engagements.find(engagementId)

      const attrs = {
        status: "Delivering",
        audiences: engagement.audiences.map((audience) => {
          if (audience.id === audienceId) {
            audience.destinations = audience.destinations.map((destination) => {
              destination.latest_delivery = {
                update_time: dayjs().toJSON(),
                status: "Delivering",
              }
              return destination
            })
          }
          return audience
        }),
      }

      engagement.update(attrs)

      return { message: "Successfully created delivery jobs" }
    }
  )

  server.post(
    "/engagements/:id/audience/:audienceId/destination/:destinationId/schedule",
    () => {
      return { message: "Successfully updated delivery schedule" }
    }
  )

  server.post(
    "/engagements/:id/audience/:audienceId/destination/:destinationId/deliver",
    () => {
      return { message: "Successfully created delivery jobs" }
    }
  )
  server.get(
    "/engagements/:id/audience/:audienceId/destination/:destinationId/campaign-mappings",
    (schema) => {
      return schema.campaignOptions.find(1)
    }
  )
  server.put(
    "/engagements/:id/audience/:audienceId/destination/:destinationId/campaigns",
    (schema, request) => {
      const engagementId = request.params.id
      const audienceId = request.params.audienceId
      const destinationId = request.params.destinationId
      const engagement = schema.engagements.find(engagementId)
      const requestData = JSON.parse(request.requestBody)

      engagement.campaign_mappings[destinationId] = requestData.campaigns
      const audience = engagement.campaign_performance[
        "adsPerformance"
      ].audience_performance.filter((aud) => aud.id === audienceId)
      if (audience.length === 1) {
        const destination = audience[0].destinations.filter(
          (dest) => dest.id === destinationId
        )
        if (destination.length === 1) {
          destination[0].campaigns = []
          const exclude = new Set(["id", "name", "destinations"])
          const countData = Object.fromEntries(
            Object.entries(audience[0]).filter(
              (entry) => !exclude.has(entry[0])
            )
          )
          Object.entries(countData).forEach(
            (entry) => (destination[0][entry[0]] = entry[1])
          )
          destination[0].is_mapped = true
          const campaigns = requestData.campaigns.map((camp) => {
            const mockCamp = { ...countData }
            mockCamp["id"] = camp.id
            mockCamp["name"] = camp.name
            return mockCamp
          })
          destination[0].campaigns.push(...campaigns)
        }
      }
      return { message: "Successfully created mappings" }
    }
  )
  //update Engagement
  server.put("/engagements/:id", (schema, request) => {
    const engagementId = request.params.id
    const requestData = JSON.parse(request.requestBody)
    if (requestData.status) {
      // deactivate engagement
      const payload = {
        status: requestData.status,
      }
      schema.engagements.find(engagementId).update(payload)
      return { message: "Successfully deactivated engagement" }
    } else {
      // updating engagement
      return schema.engagements.find(engagementId).update(requestData)
    }
  })

  server.get(
    "/engagements/:id/audience/:audienceId/destination/:destinationId/campaigns",
    (schema, request) => {
      const engagementId = request.params.id
      const destinationId = request.params.destinationId
      const engagement = schema.engagements.find(engagementId)
      return engagement.campaign_mappings[destinationId] || []
    }
  )
  server.get("/engagements/:id/delivery-history", (schema, request) => {
    const id = request.params.id
    const engagement = schema.engagements.find(id)
    const destination = schema.destinations.find(7)
    return engagement.audiences.map((audience) => {
      return {
        audience: {
          id: audience.id,
          name: audience.name,
        },
        destination: {
          id: destination.id,
          name: destination.name,
          type: destination.type,
        },
        size: audience.size,
        delivered: dayjs().toJSON(),
        match_rate: faker.datatype.number({ min: 0, max: 1, precision: 0.001 }),
      }
    })
  })

  // Audience Performances
  server.get(
    "/engagements/:id/audience-performance/email",
    (schema, request) => {
      const id = request.params.id
      const engagement = schema.engagements.find(id)
      engagement.campaign_performance["emailPerformance"] =
        engagement.campaign_performance["emailPerformance"] ||
        schema.audiencePerformances.find(id)["email_audience_performance"]
      return engagement.campaign_performance["emailPerformance"]
    }
  )
  server.get(
    "/engagements/:id/audience-performance/display-ads",
    (schema, request) => {
      const id = request.params.id
      const engagement = schema.engagements.find(id)
      engagement.campaign_performance["adsPerformance"] =
        engagement.campaign_performance["adsPerformance"] ||
        schema.audiencePerformances.find(id)["displayads_audience_performance"]
      return engagement.campaign_performance["adsPerformance"]
    }
  )
  server.get("/engagements/:id/audience-performance/download", async () => {
    // Introduced a delay of 5 seconds to
    // replicate the API delay in processing the BLOB.
    await new Promise((r) => setTimeout(r, 5000))
    return audienceCSVData
  })

  server.del("/engagements/:id", (schema, request) => {
    const id = request.params.id
    const engagement_deleted = schema.engagements.find(id)
    const engagement_deleted_name = engagement_deleted.name
    engagement_deleted.destroy()
    return "Engagement " + engagement_deleted_name + " successfully deleted"
  })

  // models
  server.get("/models")
  server.post("/models", (schema, request) => {
    let attrs = JSON.parse(request.requestBody)
    return schema.models.create(attrs)
  })

  server.get("/models/:id/overview", (schema, request) => {
    const id = request.params.id
    const data = schema.models.find(id)
    data.attrs.performance_metric = {
      rmse: -1,
      auc: 0.79,
      precision: 0.82,
      recall: 0.65,
      current_version: "3.1.2",
    }

    return data
  })

  server.get("/models/:id/feature-importance", () => {
    return featureData.featureList
  })

  server.get("/models/:id/version-history", (schema, request) => {
    const id = request.params.id
    const model = schema.models.find(id)
    return model.attrs.version_history
  })

  server.get("/models/:id/lift", () => liftData)

  server.get("/models/:id/drift", () => driftData())

  server.get("/models/:id/features", (schema, request) => {
    const id = request.params.id
    const model = schema.models.find(id)
    return model.attrs.model_feature
  })

  server.patch("/models", (schema, request) => {
    const requestData = JSON.parse(request.requestBody)
    return schema.models.find(requestData.models_ids).update(requestData.body)
  })

  server.del("/models/:id", (schema, request) => {
    const code = 200
    const headers = {}
    const id = request.params.id
    const model = schema.models.find(id)
    model.destroy()
    const body = { message: "SUCCESS" }
    return new Response(code, headers, body)
  })

  // customers
  server.get("/customers")

  server.get("/customers/:hux_id", (schema, request) => {
    const huxId = request.params.hux_id
    const attrs = schema.customers.findBy({ hux_id: huxId }).attrs
    const customerProfile = server.create("customerProfile")
    customerProfile["overview"] = { ...customerProfile["overview"], ...attrs }
    return customerProfile
  })

  server.get("/customers/overview", () => customersOverview)

  server.post("/customers/:huxId/events", () => customerEventData)

  server.get("/customers-insights/geo", () => mapData)

  server.get("/customers-insights/demo", () => demographicsData)

  server.get("/customers-insights/total", () => totalCustomersData)

  server.get("/customers-insights/revenue", () => totalCustomerSpendData)

  server.get("/customers-insights/cities", (schema, request) => {
    let batchNumber = request.queryParams["batch_number"] || 1
    let batchSize = request.queryParams["batch_size"] || 100
    let start = batchNumber === 1 ? 0 : (batchNumber - 1) * batchSize
    let end = batchNumber === 1 ? batchSize : batchNumber * batchSize
    return schema.geoCities.all().slice(start, end)
  })

  server.get("/customers-insights/states", (schema) => {
    return schema.geoStates.all()
  })

  server.get("/customers-insights/countries", (schema) => {
    return schema.geoCountries.all()
  })

  server.get("/customers", (schema, request) => {
    let currentBatch = request.queryParams.batch_number
    let batchSize = request.queryParams.batch_size
    let initialCount = currentBatch == 1 ? 0 : (currentBatch - 1) * batchSize
    let lastCount = currentBatch == 1 ? batchSize : currentBatch * batchSize
    const customers = schema.customers.all().slice(initialCount, lastCount)
    return customers
  })

  server.post("/customers/overview", () => customersOverview)

  // identity resolution
  server.get("/idr/overview", () => {
    return {
      date_range: {
        start_date: faker.date.past(5),
        end_date: dayjs().toJSON(),
      },
      overview: idrOverview(),
    }
  })
  server.get(
    "/idr/datafeeds",
    (schema) => {
      return schema.idrDataFeeds.all()
    },
    { timing: 10 }
  )
  server.get("/idr/datafeeds/:datafeed_id", () => idrDataFeedReport)
  server.get("/idr/matching-trends", () => idrMatchingTrends)

  // notifications
  server.get("/notifications", (schema, request) => {
    let currentBatch =
      request.queryParams.batch_number || request.queryParams.batchNumber
    let batchSize =
      request.queryParams.batch_size || request.queryParams.batchSize
    let initialCount = currentBatch == 1 ? 0 : (currentBatch - 1) * batchSize
    let lastCount = currentBatch == 1 ? batchSize : currentBatch * batchSize
    let allNotifications = schema.notifications.all()
    const notifications = {
      notifications: allNotifications.models.slice(initialCount, lastCount),
      total: allNotifications.length,
    }
    return notifications
  })
  server.get("/notifications/:notification_id", (schema, request) => {
    const id = request.params.notification_id
    let singleNotification = schema.notifications.find(id)
    return singleNotification
  })

  server.get("/users", (schema) => {
    return schema.users.all()
  })

  // audiences
  server.get("/audiences")

  server.get("/audiences/:id/audience_insights", () => {
    demographicsData.demo = mapData
    return demographicsData
  })
  server.get("/audiences/:id/:type", async () => {
    // Introduced a delay of 15 seconds to
    // replicate the API delay in processing the BLOB.
    await new Promise((r) => setTimeout(r, 15000))
    return audienceCSVData
  })

  server.get("/audiences/:id", (schema, request) => {
    const id = request.params.id
    const audience = schema.audiences.find(id)
    return {
      ...audience.attrs,
      audience_insights: audienceInsights,
    }
  })

  server.post("/audiences", (schema, request) => {
    const requestData = JSON.parse(request.requestBody)
    requestData.engagements = []
    requestData.destinations = []

    const now = dayjs().toJSON()

    const attrs = {
      ...requestData,
      create_time: () => now,
      created_by: me.full_name(),
      update_time: () => now,
      updated_by: me.full_name(),
    }

    return server.create("audience", attrs)
  })

  server.put("/audiences/:id", (schema, request) => {
    const audienceId = request.params.id
    const requestData = JSON.parse(request.requestBody)
    const payload = {
      name: requestData.name,
      filters: requestData.filters,
    }
    return schema.audiences.find(audienceId).update(payload)
  })

  server.post("/audiences/:id/deliver", () => {
    return { message: "Successfully created delivery jobs" }
  })

  server.get("/audiences/rules", () => attributeRules)
  server.get("/audiences/:id/delivery-history", (schema, request) => {
    const id = request.params.id
    const audience = schema.audiences.find(id)
    const destination = schema.destinations.find(id)
    return audience.engagements.map((engagement) => {
      return {
        engagement: {
          id: engagement.id,
          name: engagement.name,
        },
        destination: {
          id: destination && destination.id,
          name: destination && destination.name,
          type: destination && destination.type,
        },
        size: audience.size,
        delivered: dayjs().toJSON(),
        match_rate: faker.datatype.number({ min: 0, max: 1, precision: 0.001 }),
      }
    })
  })

  server.get("/audiences/:id/cities", (schema, request) => {
    let batchNumber = request.queryParams["batch_number"] || 1
    let batchSize = request.queryParams["batch_size"] || 100
    let start = batchNumber === 1 ? 0 : (batchNumber - 1) * batchSize
    let end = batchNumber === 1 ? batchSize : batchNumber * batchSize
    return schema.geoCities.all().slice(start, end)
  })

  server.get("/audiences/:id/states", (schema) => {
    return schema.geoStates.all()
  })

  server.get("/audiences/:id/countries", (schema) => {
    return schema.geoCountries.all()
  })

  server.del("/audiences/:id", (schema, request) => {
    const id = request.params.id
    const audience_deleted = schema.audiences.find(id)
    const audience_deleted_name = audience_deleted.name
    audience_deleted.destroy()
    return "Audience " + audience_deleted_name + " successfully deleted"
  })

  server.del("/audiences/:id/destinations", (schema, request) => {
    let requestData = JSON.parse(request.requestBody)
    const destination_deleted = schema.audiences.find(requestData.id)
    const destination_deleted_name = destination_deleted.name
    destination_deleted.destroy()
    return (
      "Standalone destination " +
      destination_deleted_name +
      " successfully deleted"
    )
  })

  //lookalike audiences
  server.post("/lookalike-audiences", (schema, request) => {
    let requestData = JSON.parse(request.requestBody)
    requestData.engagements = requestData.engagement_ids.map((id) => {
      return schema.engagements.find(id)
    })
    requestData.is_lookalike = true
    const now = dayjs().toJSON()
    const attrs = {
      ...requestData,
      create_time: now,
      created_by: me.full_name(),
      update_time: now,
      updated_by: me.full_name(),
      size: 0,
    }
    delete attrs["engagement_ids"]

    return schema.audiences.create(attrs)
  })

  server.put("/lookalike-audiences/:id", (schema, request) => {
    let requestData = JSON.parse(request.requestBody)
    return schema.audiences.find(request.params.id).update(requestData)
  })

  //configuration
  server.get("/configurations", (schema) => {
    return schema.configurations.all()
  })

  //applications
  server.get("/applications", () => {
    return applications
  })

  server.post("/applications", (schema, request) => {
    return (
      "Application " +
      JSON.parse(request.requestBody).name +
      " is successfully created"
    )
  })

  server.patch("/applications/:id", (schema, request) => {
    let app = applications.find((x) => x.id == JSON.parse(request.params.id))
    return "Application " + app.name + " is successfully updated"
  })
}
