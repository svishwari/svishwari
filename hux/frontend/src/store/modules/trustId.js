import Vue from "vue"
import api from "@/api/client"
import { handleError } from "@/utils"

const namespaced = true

const state = {
  trustIdOverview: null,
  segmentComparison: [],
  addSegment: []
}

const getters = {
  getTrustOverview: (state) => state.trustIdOverview,

  getSegmentsComparison: (state) => state.segmentComparison,

  getAddSegment: (state) => state.addSegment,
}

const mutations = {
  setTrustIdOverview(state, trustIdOverview) {
    Vue.set(state, "trustIdOverview", trustIdOverview)
  },
  SET_SEGMENT_COMPARISON(state, data) {
    Vue.set(state, "segmentComparison", data)
  },
  SET_ADD_SEGMENT(state, data) {
    Vue.set(state, "addSegment", data)
  },
}

const actions = {
  async getTrustIdOverview({ commit }) {
    try {
      const response = await api.users.trustIdOverview()
      commit("setTrustIdOverview", response.data)
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
  async getSegmentData({ commit }) {
    try {
      const response = await api.trustId.getSegments()
      commit("SET_ADD_SEGMENT", response.data)
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
