import Vue from "vue"
import api from "@/api/client"
import { handleError } from "@/utils"

const namespaced = true

const state = {
  items: {},

  overview: {},

  // TODO: to be integrated with HUS-226
  insights: null,

  totalCustomers: [],

  totalCustomerSpend: [],

  geoOverview: [],

  geoCities: [],

  geoCountries: [],

  geoStates: [],

  demographics: {},

  events: [],
}

const getters = {
  list: (state) => Object.values(state.items),

  single: (state) => (id) => state.items[id],

  overview: (state) => state.overview,

  insights: (state) => state.insights,

  totalCustomers: (state) => state.totalCustomers,

  totalCustomerSpend: (state) => state.totalCustomerSpend,

  geoOverview: (state) => state.geoOverview,

  geoCities: (state) => state.geoCities,

  geoCountries: (state) => state.geoCountries,

  geoStates: (state) => state.geoStates,

  demographics: (state) => state.demographics,

  getEvents: (state) => state.events,
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
    Vue.set(state.items, item["overview"]["hux_id"], item)
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

  ADD_GEO_CITIES(state, data) {
    state.geoCities.push(...data)
  },

  SET_GEO_STATES(state, data) {
    state.geoStates = data
  },

  SET_TOTAL_CUSTOMERS(state, data) {
    state.totalCustomers = data
  },

  SET_TOTAL_CUSTOMER_SPEND(state, data) {
    state.totalCustomerSpend = data
  },

  SET_DEMOGRAPHICS(state, data) {
    state.demographics = data
  },

  SET_CUSTOMER_EVENTS(state, data) {
    state.events = data
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

  async getRedact({ commit }, params) {
    try {
      const response = await api.customers.getRedact(
        params.id,
        params.redactFlag
      )
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

  async getGeoCities({ commit }, { batchNumber, batchSize }) {
    try {
      if (batchNumber === 1) commit("SET_GEO_CITIES", [])
      const response = await api.customers.geoCities(batchNumber, batchSize)
      commit("ADD_GEO_CITIES", response.data)
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
      commit("SET_TOTAL_CUSTOMERS", response.data)
    } catch (error) {
      handleError(error)
      throw error
    }
  },

  async getCustomerSpend({ commit }) {
    try {
      const response = await api.customers.getCustomerSpend()
      commit("SET_TOTAL_CUSTOMER_SPEND", response.data)
    } catch (error) {
      handleError(error)
      throw error
    }
  },

  async getDemographics({ commit }, data) {
    try {
      const response = await api.customers.demographics(data)
      commit("SET_DEMOGRAPHICS", response.data)
    } catch (error) {
      handleError(error)
      throw error
    }
  },

  async getCustomerEvents({ commit }, id) {
    try {
      const response = await api.customers.events(id)
      commit("SET_CUSTOMER_EVENTS", response.data)
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
