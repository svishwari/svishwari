import api from "@/api/client"
import { handleError } from "@/utils"

const namespaced = true

const state = {
  items: {},
  overview: {},
}

const getters = {
  list: (state) => Object.values(state.items),
  overview: (state) => state.overview,
}

const mutations = {
  SET_ALL(state, items) {
    state.items = items
  },

  SET_OVERVIEW(state, data) {
    state.overview = data
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
}

export default {
  namespaced,
  state,
  getters,
  mutations,
  actions,
}
