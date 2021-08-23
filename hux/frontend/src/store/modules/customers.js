import Vue from "vue"
import api from "@/api/client"
import { handleError } from "@/utils"

const namespaced = true

const state = {
  items: {},

  overview: {},

  // TODO: to be integrated with HUS-226
  insights: null,

  geographics: [],

  total_customers: [],
  
  geoOverview: [],

  geoCities: [],

  geoCountries: [],

  geoStates: [],
}

const getters = {
  list: (state) => Object.values(state.items),

  single: (state) => (id) => state.items[id],

  overview: (state) => state.overview,

  insights: (state) => state.insights,

  geographics: (state) => state.geographics,

  total_customers: (state) => state.total_customers,
  
  geoOverview: (state) => state.geoOverview,

  geoCities: (state) => state.geoCities,

  geoCountries: (state) => state.geoCountries,

  geoStates: (state) => state.geoStates,
}

const mutations = {
  SET_ALL(state, items) {
    items.forEach((item) => {
      Vue.set(state.items, item.hux_id, item)
    })
  },

  RESET_ALL(state) {
    Vue.set(state, "items", {})
  },

  SET_ONE(state, item) {
    Vue.set(state.items, item.hux_id, item)
  },

  SET_OVERVIEW(state, data) {
    state.overview = data
  },

  SET_GEO_OVERVIEW(state, data) {
    state.geoOverview = data
  },

  SET_GEO_COUNTRIES(state, data) {
    state.geoCountries = data
  },

  SET_GEO_CITIES(state, data) {
    state.geoCities = data
  },

  SET_GEO_STATES(state, data) {
    state.geoStates = data
  },

  SET_TOTALCUSTOMERS(state, data) {
    state.total_customers = data
  },
}

const actions = {
  async getAll({ commit }, batchDetails) {
    try {
      if (!batchDetails.isLazyLoad) {
        commit("RESET_ALL")
      }
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

  async getGeoOverview({ commit }) {
    try {
      const response = await api.customers.geoOverview()
      commit("SET_GEO_OVERVIEW", response.data)
    } catch (error) {
      handleError(error)
      throw error
    }
  },

  async getGeoCities({ commit }) {
    try {
      const response = await api.customers.geoCities()
      commit("SET_GEO_CITIES", response.data)
    } catch (error) {
      handleError(error)
      throw error
    }
  },

  async getGeoCountries({ commit }) {
    try {
      const response = await api.customers.geoCountries()
      commit("SET_GEO_COUNTRIES", response.data)
    } catch (error) {
      handleError(error)
      throw error
    }
  },

  async getGeoStates({ commit }) {
    try {
      const response = await api.customers.geoStates()
      commit("SET_GEO_STATES", response.data)
    } catch (error) {
      handleError(error)
      throw error
    }
  },

  async getTotalCustomers({ commit }) {
    try {
      const response = await api.customers.totalCustomers()
      commit("SET_TOTALCUSTOMERS", response.data)
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
