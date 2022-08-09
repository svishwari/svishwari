import Vue from "vue"
import api from "@/api/client"
import { handleError } from "@/utils"

const namespaced = true

const state = {
  clientProjects: [],
  clientData: {},
}

const getters = {
  getClients: (state) => state.clientProjects,

  clientAppData: (state) => state.clientData,
}

const mutations = {
  SET_CLIENT_PROJECTS(state, clientProjects) {
    Vue.set(state, "clientProjects", clientProjects)
  },
  SET_CLIENT_APP_DATA(state, items) {
    Vue.set(state, "clientData", items)
  },
}

const actions = {
  async getClientProjects({ commit }) {
    try {
      const response = await api.clients.all()
      commit("SET_CLIENT_PROJECTS", response.data)
    } catch (error) {
      handleError(error)
      throw error
    }
  },
  async getClientAppData({ commit }) {
    try {
      const response = await api.clients.clientData()
      commit("SET_CLIENT_APP_DATA", response.data)
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
