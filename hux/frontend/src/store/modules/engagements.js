import Vue from "vue"
import api from "@/api/client"
import { handleError } from "@/utils"

const namespaced = true

const state = {
  items: {},
  audiencePerformance: {},
}

const getters = {
  list: (state) => Object.values(state.items),
  audiencePerformanceByAds: (state) => state.audiencePerformance.ads,
  audiencePerformanceByEmail: (state) => state.audiencePerformance.email,
}

const mutations = {
  SET_ALL(state, items) {
    items.forEach((item) => {
      item.audienceList = []
      item.status = String(item.status).toLowerCase()
      Vue.set(state.items, item.id, item)
    })
  },

  SET_ONE(state, item) {
    Vue.set(state.items, item.id, item)
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
    console.log(payload.data);
    state.items[payload.id].audienceList = payload.data
  }
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
                end_date: "",
                start_date: "",
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

  updateAudienceList({ commit }, payload) {
    commit('SET_AUDIENCE_LIST', payload);
  },
}

export default {
  namespaced,
  state,
  getters,
  mutations,
  actions,
}
