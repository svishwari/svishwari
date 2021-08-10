import Vue from "vue"
import api from "@/api/client"
import { handleError } from "@/utils"

const namespaced = true

const state = {
  items: {},

  overview: {},

  // TODO: to be integrated with HUS-226
  insights: null,
}

const getters = {
  list: (state) => Object.values(state.items),

  single: (state) => (id) => state.items[id],

  overview: (state) => state.overview,

  insights: (state) => state.insights,
}

const mutations = {
  SET_ALL(state, items) {
    items.forEach((item) => {
      Vue.set(state.items, item.hux_id, item)
    })
  },

  SET_ONE(state, item) {
    Vue.set(state.items, item.hux_id, item)
  },

  SET_OVERVIEW(state, data) {
    state.overview = data
  },
}

const actions = {
  async getAll({ commit }, batchDetails) {
    try {
      const response = await api.customers.getCustomers(
        batchDetails.batchSize,
        batchDetails.batchNumber
      )
      commit("SET_ALL", response.data.customers)
    } catch (error) {
      handleError(error)
      throw error
    }
  },

  async get({ commit }, id) {
    try {
      const response = await api.customers.find(id)
      commit("SET_ONE", response.data)
    } catch (error) {
      handleError(error)
      throw error
    }
  },

  async getOverview({ commit }) {
    try {
      const response = await api.customers.overview()
      commit("SET_OVERVIEW", response.data)
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
