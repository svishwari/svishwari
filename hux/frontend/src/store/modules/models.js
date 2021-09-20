import Vue from "vue"
import api from "@/api/client"
import { handleError } from "@/utils"

const namespaced = true

const state = {
  items: {},
  overview: {},
  history: {},
  lift: [],
  features: [],
  drift: [],
  modelFeatures: [],
}

const getters = {
  list: (state) => Object.values(state.items),
  single: (state) => (id) => state.items[`_${id}`],
  overview: (state) => state.overview,
  history: (state) => Object.values(state.history),
  lift: (state) => state.lift,
  features: (state) => state.features,
  drift: (state) => state.drift,
  modelFeatures: (state) => {
    return state.modelFeatures.map((feature) => {
      return {
        name: feature.name,
        feature_service: feature.feature_service,
        data_source: feature.data_source,
        status: feature.status,
        popularity: feature.popularity,
        created_by: feature.created_by,
      }
    })
  },
}

const mutations = {
  SET_ALL(state, items) {
    items.forEach((item) => {
      // appending _ converts id from numeric to string which helps in preserving the order of the keys
      // the order is changed incase the keys of the object are numeric and preserved incase of string
      Vue.set(state.items, `_${item.id}`, item)
    })
  },

  SET_OVERVIEW(state, data) {
    state.overview = data
  },

  SET_FEATURES(state, data) {
    state.features = data
  },

  SET_DRIFT(state, data) {
    state.drift = data
  },

  SET_HISTORY(state, items) {
    let getHistory = items.sort(function (a, b) {
      return a.version === b.version ? 0 : a.version > b.version ? -1 : 1
    })
    getHistory[0]["current"] = true
    getHistory.forEach((item) => {
      Vue.set(state.history, item.version, item)
    })
  },
  SET_MODAL_FEATURE(state, data) {
    state.modelFeatures = data
  },
  SET_LIFT(state, data) {
    state.lift = data
  },
}

const actions = {
  async getAll({ commit }) {
    try {
      const response = await api.models.all()
      commit("SET_ALL", response.data)
    } catch (error) {
      handleError(error)
      throw error
    }
  },

  async getOverview({ commit }, type) {
    try {
      const response = await api.models.overview(type)
      commit("SET_OVERVIEW", response.data)
    } catch (error) {
      handleError(error)
      throw error
    }
  },

  async getFeatures({ commit }, type) {
    try {
      const response = await api.models.features(type)
      commit("SET_FEATURES", response.data)
    } catch (error) {
      handleError(error)
      throw error
    }
  },

  async getHistory({ commit }, modelId) {
    try {
      const response = await api.models.versionHistory(modelId)
      commit("SET_HISTORY", response.data)
    } catch (error) {
      handleError(error)
      throw error
    }
  },

  async getModelFeatures({ commit }, modelId) {
    try {
      const response = await api.models.modelFeatures(modelId)
      commit("SET_MODAL_FEATURE", response.data)
    } catch (error) {
      handleError(error)
      throw error
    }
  },

  async getLift({ commit }, modelId) {
    try {
      const response = await api.models.lift(modelId)
      commit("SET_LIFT", response.data)
    } catch (error) {
      handleError(error)
      throw error
    }
  },

  async getDrift({ commit }, modelId) {
    try {
      const response = await api.models.drift(modelId)
      commit("SET_DRIFT", response.data)
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
