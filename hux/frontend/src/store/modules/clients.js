import Vue from "vue"
import api from "@/api/client"
import { handleError } from "@/utils"

const namespaced = true

const state = {
  clientProjects: [],
}

const mutations = {
  SET_CLIENT_PROJECTS(state, clientProjects) {
    Vue.set(state, "clientProjects", clientProjects)
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
}

const getters = {
  getClients: (state) => state.clientProjects,
}

export default {
  namespaced,
  state,
  getters,
  mutations,
  actions,
}
