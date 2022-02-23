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
  pipelinePreformance: {},
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
  singlePipeline: (state) => state.pipelinePreformance,
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
  SET_ONE(state, item) {
    Vue.set(state.items, `_${item.id}`, item)
  },
  REMOVE_MODEL(state, id) {
    Vue.delete(state.items, `_${id}`)
  },
  SET_ONE_PIPELINE(state, item) {
    state.pipelinePreformance = item
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

  async getOverview({ commit }, model) {
    try {
      let response
      if (model.version) {
        response = await api.models.overview(model.id, model.version)
      } else {
        response = await api.models.overview(model.id)
      }
      commit("SET_OVERVIEW", response.data)
    } catch (error) {
      handleError(error)
      throw error
    }
  },

  async getFeatures({ commit }, model) {
    try {
      let response
      if (model.version) {
        response = await api.models.features(model.id, model.version)
      } else {
        response = await api.models.features(model.id)
      }
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

  async getModelFeatures({ commit }, model) {
    try {
      let response
      if (model.version) {
        response = await api.models.modelFeatures(model.id, model.version)
      } else {
        response = await api.models.modelFeatures(model.id)
      }
      commit("SET_MODAL_FEATURE", response.data)
    } catch (error) {
      handleError(error)
      throw error
    }
  },

  async getLift({ commit }, model) {
    try {
      let response
      if (model.version) {
        response = await api.models.lift(model.id, model.version)
      } else {
        response = await api.models.lift(model.id)
      }
      commit("SET_LIFT", response.data)
    } catch (error) {
      handleError(error)
      throw error
    }
  },

  async getDrift({ commit }, model) {
    try {
      let response
      if (model.version) {
        response = await api.models.drift(model.id, model.version)
      } else {
        response = await api.models.drift(model.id)
      }
      commit("SET_DRIFT", response.data)
    } catch (error) {
      handleError(error)
      throw error
    }
  },

  clearModelValues({ commit }) {
    commit("SET_DRIFT", [])
    commit("SET_LIFT", [])
    commit("SET_MODAL_FEATURE", [])
    commit("SET_FEATURES", [])
    commit("SET_OVERVIEW", {})
  },

  async batchUpdate({ commit }, dataSources) {
    try {
      const response = await api.models.batchUpdate(dataSources)
      response.data.forEach((each) => {
        commit("SET_ONE", each)
      })
    } catch (error) {
      handleError(error)
      throw error
    }
  },

  async add({ commit }, model) {
    try {
      const response = await api.models.create(model)
      commit("SET_ONE", response.data)
      return response.data
    } catch (error) {
      handleError(error)
      throw error
    }
  },
  async remove({ commit }, model) {
    try {
      const response = await api.models.remove(model)
      commit("REMOVE_MODEL", model.id)
      return response.data
    } catch (error) {
      handleError(error)
      throw error
    }
  },
  async getPipelinePreformance({ commit }, modelId) {
    try {
      const response = await api.models.getPipePerfomance(modelId)
      commit("SET_ONE_PIPELINE", response.data)
      return response.data
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
