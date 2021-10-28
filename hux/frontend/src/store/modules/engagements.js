import Vue from "vue"
import api from "@/api/client"
import { handleError } from "@/utils"
import dayjs from "dayjs"

const namespaced = true

const state = {
  items: {},

  audiencePerformance: {
    ads: {},
    email: {},
  },

  deliveries: {},

  filteredDeliveries: [],

  campaignMappingOptions: {},
  campaignMappings: [],
}

const getters = {
  list: (state) => Object.values(state.items),

  engagement: (state) => (id) => state.items[id],

  deliveries: (state) => (id) => {
    const deliveries = state.deliveries[id]
    return deliveries ? Object.values(state.deliveries[id]) : []
  },

  filteredDeliveries: (state) => state.filteredDeliveries,

  audiencePerformanceByAds: (state) => state.audiencePerformance.ads,

  audiencePerformanceByEmail: (state) => state.audiencePerformance.email,

  campaignMappingOptions: (state) => state.campaignMappingOptions,
  campaignMapping: (state) => (id) => {
    return state.campaignMappings[id]
  },
}

const mutations = {
  SET_ALL(state, items) {
    items.forEach((item) => {
      item.audienceList = []
      item.isCurrentRow = false
      Vue.set(state.items, item.id, item)
    })
  },

  SET_ONE(state, item) {
    Vue.set(state.items, item.id, item)
  },

  SET_DELIVERIES(state, { engagementId, deliveries }) {
    Vue.set(state.deliveries, engagementId, deliveries)
  },

  SET_AUDIENCE_PERFORMANCE(state, { item, type }) {
    /**
     * TODO To be revised with actual API call once API is ready for integration.
     * Below logic needs revision
     */
    let audiencePerformanceObject = {}
    if (type === "ads") {
      audiencePerformanceObject = item
    } else {
      audiencePerformanceObject = item
    }
    Vue.set(state.audiencePerformance, type, audiencePerformanceObject)
  },

  SET_AUDIENCE_LIST(state, payload) {
    let engagement = state.items[payload.id]
    if (engagement.audienceList.length == 0) {
      engagement.audienceList = payload.data
      engagement.isCurrentRow = false
    }
  },

  MARK_CURRENT_ROW(state, id) {
    state.items[id].isCurrentRow = !state.items[id].isCurrentRow
  },

  SET_CAMPAIGN_MAPPINGS(state, payload) {
    if (Object.keys(payload).length > 0) {
      state.campaignMappingOptions = {
        campaigns: payload.campaigns,
        delivery_jobs: payload.delivery_jobs.map((job) => ({
          ...job,
          name: dayjs(job.created_time).format("MM/D/YYYY hh:ssA"),
        })),
      }
    } else {
      state.campaignMappingOptions = {}
    }
  },
  SET_CAMPAIGNS(state, data) {
    Vue.set(state.campaignMappings, data.id, data.payload)
  },

  SET_FILTERED_DELIVERIES(state, deliveries) {
    state.filteredDeliveries = deliveries
  },

  REMOVE_ENGAGEMENT(state, id) {
    Vue.delete(state.items, id)
  },
}

const actions = {
  async getAll({ commit }) {
    try {
      const response = await api.engagements.all()
      commit("SET_ALL", response.data)
    } catch (error) {
      handleError(error)
      throw error
    }
  },

  async get({ commit }, id) {
    try {
      const response = await api.engagements.find(id)
      commit("SET_ONE", response.data)
    } catch (error) {
      handleError(error)
      throw error
    }
  },

  async getDeliveries({ commit }, engagementId) {
    try {
      const response = await api.engagements.deliveries(engagementId)
      commit("SET_DELIVERIES", {
        engagementId: engagementId,
        deliveries: response.data,
      })
    } catch (error) {
      handleError(error)
      throw error
    }
  },

  async getAudiencePerformance({ commit }, payload) {
    const response = await api.engagements.fetchAudiencePerformance(
      payload.id,
      payload.type
    )
    commit("SET_AUDIENCE_PERFORMANCE", {
      item: response.data,
      type: payload.type,
    })
  },

  async fetchAudienceMetrics(_, { id }) {
    try {
      const response = await api.engagements.downloadAudienceMetrics(id)
      return response
    } catch (error) {
      handleError(error)
      throw error
    }
  },

  async deliverySchedule(_, requestPayload) {
    try {
      const payload = requestPayload
      await api.engagements.deliverySchedule(payload)
    } catch (error) {
      handleError(error)
      throw error
    }
  },

  async add({ commit }, engagement) {
    try {
      const payload = {
        name: engagement.name,

        description: engagement.description,
        delivery_schedule:
          engagement.delivery_schedule === null
            ? null
            : {
                schedule: engagement.delivery_schedule.schedule,
                end_date: engagement.delivery_schedule.end_date,
                start_date: engagement.delivery_schedule.start_date,
              },
        audiences: Object.values(engagement.audiences).map((audience) => {
          return {
            id: audience.id,
            destinations: audience.destinations,
          }
        }),
      }
      const response = await api.engagements.create(payload)
      commit("SET_ONE", response.data)
      return response.data
    } catch (error) {
      handleError(error)
      throw error
    }
  },

  async update({ commit }, engagement) {
    try {
      const response = await api.engagements.update(
        engagement.id,
        engagement.name,
        engagement.desciption
      )
      commit("SET_ONE", response.data)
    } catch (error) {
      handleError(error)
      throw error
    }
  },

  async remove({ commit }, engagement) {
    try {
      await api.engagements.remove(engagement.id)
      commit("REMOVE_ENGAGEMENT", engagement.id)
    } catch (error) {
      handleError(error)
      throw error
    }
  },

  async deliver(_, id) {
    try {
      await api.engagements.deliver(id)
    } catch (error) {
      handleError(error)
      throw error
    }
  },

  async deliverAudience(_, { id, audienceId }) {
    try {
      await api.engagements.deliverAudience({
        resourceId: id,
        audienceId: audienceId,
      })
    } catch (error) {
      handleError(error)
      throw error
    }
  },

  async getFilteredDeliveries({ commit }, data) {
    try {
      const response = await api.engagements.deliveries(data.id, data.query)
      commit("SET_FILTERED_DELIVERIES", response.data || [])
    } catch (error) {
      handleError(error)
      throw error
    }
  },

  async deliverAudienceDestination(_, { id, audienceId, destinationId }) {
    try {
      await api.engagements.deliverAudienceDestination({
        resourceId: id,
        audienceId: audienceId,
        destinationId: destinationId,
      })
    } catch (error) {
      handleError(error)
      throw error
    }
  },
  async fetchCampaignMappings({ commit }, { id, audienceId, destinationId }) {
    try {
      const response = await api.engagements.getCampaignMappingOptions({
        resourceId: id,
        audienceId: audienceId,
        destinationId: destinationId,
      })
      commit("SET_CAMPAIGN_MAPPINGS", response.data)
    } catch (error) {
      commit("SET_CAMPAIGN_MAPPINGS", {})
      handleError(error)
      throw error
    }
  },
  async getCampaigns({ commit }, { id, audienceId, destinationId }) {
    try {
      const response = await api.engagements.getCampaigns({
        resourceId: id,
        audienceId: audienceId,
        destinationId: destinationId,
      })
      commit("SET_CAMPAIGNS", { id: destinationId, payload: response.data })
    } catch (error) {
      handleError(error)
      throw error
    }
  },
  async attachAudience(_, { engagementId, data }) {
    try {
      await api.engagements.attachAudience(engagementId, data)
    } catch (error) {
      handleError(error)
      throw error
    }
  },
  async detachAudience(_, { engagementId, data }) {
    try {
      await api.engagements.detachAudience(engagementId, data)
    } catch (error) {
      handleError(error)
      throw error
    }
  },
  async attachAudienceDestination(_, { engagementId, audienceId, data }) {
    try {
      await api.engagements.attachDestination(engagementId, audienceId, data)
    } catch (error) {
      handleError(error)
      throw error
    }
  },
  async detachAudienceDestination(_, { engagementId, audienceId, data }) {
    try {
      await api.engagements.detachDestination(engagementId, audienceId, data)
    } catch (error) {
      handleError(error)
      throw error
    }
  },
  async saveCampaignMappings(_, { id, audienceId, destinationId, data }) {
    try {
      await api.engagements.updateCampaignMapping(
        {
          resourceId: id,
          audienceId: audienceId,
          destinationId: destinationId,
        },
        data
      )
    } catch (error) {
      handleError(error)
      throw error
    }
  },
  //update Engagement
  async updateEngagement(_, { id, data }) {
    try {
      await api.engagements.update(id, data)
    } catch (error) {
      handleError(error)
      throw error
    }
  },

  updateAudienceList({ commit }, payload) {
    commit("SET_AUDIENCE_LIST", payload)
  },

  markCurrentRow({ commit }, id) {
    commit("MARK_CURRENT_ROW", id)
  },
}

export default {
  namespaced,
  state,
  getters,
  mutations,
  actions,
}
