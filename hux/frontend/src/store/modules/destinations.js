import Vue from "vue"
import api from "@/api/client"
import { handleError } from "@/utils"

const namespaced = true

const state = {
  items: {},
  constants: {},
}

const getters = {
  list: (state) => Object.values(state.items),

  single: (state) => (id) => state.items[id],

  enabledDestination: (state) =>
    Object.values(state.items).filter((item) => item.is_enabled),

  constants: (state) => state.constants,
}

const mutations = {
  SET_ALL(state, items) {
    items.forEach((item) => {
      // TODO: remove this once ORCH-233 is addressed
      if (item.type === "SFMC") item.type = "salesforce"
      item.type = String(item.type).toLowerCase()
      Vue.set(state.items, item.id, item)
    })
  },

  SET_ONE(state, item) {
    // TODO: remove this once ORCH-233 is addressed
    if (item.type === "SFMC") item.type = "salesforce"
    item.type = String(item.type).toLowerCase()
    Vue.set(state.items, item.id, item)
  },

  SET_CONSTANTS(state, data) {
    Vue.set(state, "constants", data)
  },
}

const actions = {
  async getAll({ commit }) {
    try {
      const response = await api.destinations.all()
      commit("SET_ALL", response.data)
    } catch (error) {
      handleError(error)
      throw error
    }
  },

  async get({ commit }, id) {
    try {
      const response = await api.destinations.find(id)
      commit("SET_ONE", response.data)
    } catch (error) {
      handleError(error)
      throw error
    }
  },

  async add({ commit }, destination) {
    try {
      const body = {
        authentication_details: destination.authentication_details,
      }
      if (
        Object.prototype.hasOwnProperty.call(
          destination,
          "performance_metrics_data_extension"
        )
      ) {
        body.performance_metrics_data_extension =
          destination.performance_metrics_data_extension
      }
      const response = await api.destinations.update(destination.id, body)
      commit("SET_ONE", response.data)
    } catch (error) {
      handleError(error)
      throw error
    }
  },

  async validate(_, destination) {
    try {
      const body = {
        type: destination.type,
        authentication_details: destination.authentication_details,
      }
      const response = await api.destinations.validate(body)
      return response.data
    } catch (error) {
      handleError(error)
      throw error
    }
  },

  async constants({ commit }) {
    try {
      const response = await api.destinations.constants()
      commit("SET_CONSTANTS", response.data)
    } catch (error) {
      handleError(error)
      throw error
    }
  },
}

export default {
  namespaced,
  state,
  getters,
  mutations,
  actions,
}
