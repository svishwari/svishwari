import Vue from "vue"
import api from "@/api/client"
import { handleError } from "@/utils"

const namespaced = true

const state = {
  configurationModels: [],
}

const getters = {
  configurationModels: (state) => {
    return state.configurationModels
  },
}

const mutations = {
  setConfigurationModels(state, models) {
    Vue.set(state, "configurationModels", models)
  },
}

const actions = {
  async getConfigModels({ commit }) {
    try {
      const result = await api.configurations.all()
      commit("setConfigurationModels", result.data)
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
