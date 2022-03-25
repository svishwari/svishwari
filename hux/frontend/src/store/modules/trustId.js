import Vue from "vue"
import api from "@/api/client"
import { handleError } from "@/utils"

const namespaced = true

const state = {
  trustIdOverview: null,
  segmentComparison: [],
}

const getters = {
  getTrustOverview: (state) => state.trustIdOverview,

  getSegmentsComparison: (state) => state.segmentComparison,
}

const mutations = {
  setTrustIdOverview(state, trustIdOverview) {
    Vue.set(state, "trustIdOverview", trustIdOverview)
  },
  SET_SEGMENT_COMPARISON(state, data) {
    Vue.set(state, "segmentComparison", data)
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
}

export default {
  namespaced,
  state,
  getters,
  mutations,
  actions,
}
