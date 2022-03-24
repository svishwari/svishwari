import Vue from "vue"
import api from "@/api/client"
import { handleError } from "@/utils"

const namespaced = true

const state = {
  segmentComparison: [],
}

const getters = {
  getSegmentsComparison: (state) => state.segmentComparison,
}

const mutations = {
  SET_SEGMENT_COMPARISON(state, data) {
    Vue.set(state, "segmentComparison", data)
  },
}

const actions = {
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
