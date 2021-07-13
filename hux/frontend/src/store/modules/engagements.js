import Vue from "vue"
import api from "@/api/client"
import { handleError } from "@/utils"

const namespaced = true

const state = {
  items: {},

  audiencePerformance: {},

  deliveries: {},
}

const getters = {
  list: (state) => Object.values(state.items),

  engagement: (state) => (id) => state.items[id],

  deliveries: (state) => (id) => {
    const deliveries = state.deliveries[id]
    return deliveries ? Object.values(state.deliveries[id]) : []
  },

  audiencePerformanceByAds: (state) => state.audiencePerformance.ads,

  audiencePerformanceByEmail: (state) => state.audiencePerformance.email,
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

  async add({ commit }, engagement) {
    try {
      const payload = {
        name: engagement.name,

        description: engagement.description,

        delivery_schedule:
          engagement.delivery_schedule === 0
            ? null
            : {
                end_date: engagement.end_date,
                start_date: engagement.start_date,
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
