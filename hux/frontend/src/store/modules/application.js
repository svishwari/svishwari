import Vue from "vue"
import api from "@/api/client"
import { handleError } from "@/utils"

const namespaced = true

const state = {
  applications: [],
}

const getters = {
  list: (state) => Object.values(state.applications),
}

const mutations = {
  SET_APPLICATIONS(state, res) {
    Vue.set(state, "applications", res)
  },
}

const actions = {
  async getApplications({ commit }, data = { onlyActive: false }) {
    try {
      let result = await api.applications.getActiveApplications(data.onlyActive)
      commit("SET_APPLICATIONS", result.data)
    } catch (error) {
      handleError(error)
      throw error
    }
  },

  async createApplication(_, data) {
    try {
      await api.applications.createApplication(data)
    } catch (error) {
      handleError(error)
      throw error
    }
  },

  async updateApplications(_, { id, data }) {
    try {
      await api.applications.updateApplication(id, data)
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
