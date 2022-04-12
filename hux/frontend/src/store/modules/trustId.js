import Vue from "vue"
import api from "@/api/client"
import { handleError } from "@/utils"

const namespaced = true

const state = {
  trustIdOverview: null,
  segmentComparison: [],
  addSegment: [],
  trustIdAttributes: [],
}

const getters = {
  getTrustOverview: (state) => state.trustIdOverview,

  getSegmentsComparison: (state) => state.segmentComparison,

  getAddSegment: (state) => state.addSegment,

  getTrustAttributes: (state) => state.trustIdAttributes,
}

const mutations = {
  SET_TRUSTID_OVERVIEW(state, trustIdOverview) {
    Vue.set(state, "trustIdOverview", trustIdOverview)
  },
  SET_SEGMENT_COMPARISON(state, data) {
    Vue.set(state, "segmentComparison", data)
  },
  SET_ADD_SEGMENT(state, data) {
    Vue.set(state, "addSegment", data)
  },
  SET_TRUST_ATTRIBUTES(state, trustIdAttributes) {
    Vue.set(state, "trustIdAttributes", trustIdAttributes)
  },
  REMOVE_SEGMENT(state, name) {
    Vue.delete(state, name)
  },
}

const actions = {
  async getTrustIdOverview({ commit }) {
    try {
      const response = await api.trustId.trustIdOverview()
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
  async getSegmentData({ commit }) {
    try {
      const response = await api.trustId.getSegments()
      commit("SET_ADD_SEGMENT", response.data)
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
  async getTrustAttributes({ commit }) {
    try {
      const response = await api.trustId.getAttributes()
      commit("SET_TRUST_ATTRIBUTES", response)
    } catch (error) {
      handleError(error)
      throw error
    }
  },

  async removeSegment({ commit }, { segment_name }) {
    try {
      const payload = {
        segment_name: segment_name,
      }
      const response = await api.trustId.removeSegmentData(payload)
      commit("REMOVE_SEGMENT", response.data)
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
