import Vue from "vue"
import api from "@/api/client"
import { handleError } from "@/utils"

const namespaced = true

const state = {
  trustIdOverview: null,
}

const mutations = {
  setTrustIdOverview(state, trustIdOverview) {
    Vue.set(state, "trustIdOverview", trustIdOverview)
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
}

const getters = {
  getTrustOverview: (state) => state.trustIdOverview,
}
export default {
  namespaced,
  state,
  getters,
  mutations,
  actions,
}
