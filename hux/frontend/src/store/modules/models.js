import Vue from "vue"
import api from "@/api/client"
import { handleError } from "@/utils"

const namespaced = true

const state = {
  items: {},
  overview: {},
  history: [],
}

const getters = {
  list: (state) => Object.values(state.items),
  overview: (state) => state.overview,
  history: (state) => Object.values(state.history),
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

  SET_HISTORY(state, item) {
    Vue.set(state.history, item.id, item)
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

  async getHistory({ commit }, modelId) {
    try {
      const response = await api.models.versionHistory(modelId)
      commit("SET_HISTORY", response.data)
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
