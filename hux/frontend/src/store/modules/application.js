import Vue from "vue"
import api from "@/api/client"
import { handleError } from "@/utils"

const namespaced = true

const state = {
  applications: [],
  addedApplications: [],
}

const getters = {
  list: (state) => Object.values(state.applications),
  addedList: (state) => Object.values(state.addedApplications),
}

const mutations = {
  SET_APPLICATIONS(state, res) {
    Vue.set(state, "applications", res)
  },
  SET_ADDED_APPLICATIONS(state, res) {
    Vue.set(state, "addedApplications", res)
  },
}

const actions = {
  async getApplications({ commit }) {
    try {
      let result = await api.applications.getActiveApplications(false)
      commit("SET_APPLICATIONS", result.data)
    } catch (error) {
      handleError(error)
      throw error
    }
  },
  async getAddedApplications({ commit }) {
    try {
      let result = await api.applications.getActiveApplications(true)
      commit("SET_ADDED_APPLICATIONS", result.data)
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
