import Vue from "vue"
import api from "@/api/client"
import { handleError } from "@/utils"

const namespaced = true

const state = {
  items: {},
  constants: {},
  availableDestinations: {},
  dataExtensions: [],
}

const getters = {
  list: (state) => Object.values(state.items),

  single: (state) => (id) => state.items[id],

  enabledDestination: (state) =>
    Object.values(state.items).filter((item) => item.is_enabled),

  constants: (state) => state.constants,

  availableDestinations: (state) => Object.values(state.availableDestinations),

  dataExtensions: (state) => Object.values(state.dataExtensions),
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
  // TODO: Redesign this solution as this is a workaround for the destinations drawer on the audience setup page
  SET_AVAILABLE_DESTINATIONS(state, items) {
    items.forEach((item) => {
      if (item.is_added) {
        item.is_added = false
        Vue.set(state.availableDestinations, item.id, item)
      }
    })
  },
  SET_DATAEXTENSIONS(state, items) {
    items.forEach((item) => {
      Vue.set(state.dataExtensions, item.id, item)
    })
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
      await api.destinations.validate(body)
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

  async getAvailableDestinations({ commit }) {
    try {
      const response = await api.destinations.all()
      commit("SET_AVAILABLE_DESTINATIONS", response.data)
    } catch (error) {
      handleError(error)
      throw error
    }
  },

  async dataExtensions({ commit }, id) {
    try {
      const response = await api.destinations.dataExtensions(id)
      commit("SET_DATAEXTENSIONS", response.data)
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
