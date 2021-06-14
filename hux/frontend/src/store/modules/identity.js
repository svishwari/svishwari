import api from "@/api/client"
import { handleError } from "@/utils"

const namespaced = true

const state = {
  overview: {},
}

const getters = {
  overview: (state) => state.overview,
}

const mutations = {
  SET_OVERVIEW(state, data) {
    state.overview = data
  },
}

const actions = {
  async getOverview({ commit }) {
    try {
      const response = await api.identity.overview()
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
