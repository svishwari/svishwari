import Vue from "vue"
import api from "@/api/client"
import { handleError } from "@/utils"

const namespaced = true

const state = {
  trustIdOverview: null,
  segmentComparison: [],
  userFilters: [],
}

const getters = {
  getTrustOverview: (state) => state.trustIdOverview,

  getSegmentsComparison: (state) => state.segmentComparison,

  getFilters: (state) => state.userFilters,
}

const mutations = {
  SET_TRUSTID_OVERVIEW(state, trustIdOverview) {
    Vue.set(state, "trustIdOverview", trustIdOverview)
  },
  SET_SEGMENT_COMPARISON(state, data) {
    Vue.set(state, "segmentComparison", data)
  },
  SET_USER_FILTERS(state, data) {
    Vue.set(state, "userFilters", data)
  },
}

const actions = {
  async getTrustIdOverview({ commit }) {
    try {
      const response = await api.users.trustIdOverview()
      commit("SET_TRUSTID_OVERVIEW", response.data)
    } catch (error) {
      handleError(error)
      throw error
    }
  },
  async getTrustIdComparison({ commit }) {
    try {
      const response = await api.trustId.getComparison()
      commit("SET_SEGMENT_COMPARISON", response.data)
    } catch (error) {
      handleError(error)
      throw error
    }
  },
  async getUserFilters({ commit }) {
    try {
      const response = await api.trustId.getUserFilters()
      commit("SET_USER_FILTERS", response.data)
    } catch (error) {
      handleError(error)
      throw error
    }
  },
  async addSegment({ commit }, payload) {
    try {
      const response = await api.trustId.addSegment(payload)
      commit("SET_SEGMENT_COMPARISON", response.data)
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
