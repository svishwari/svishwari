import Vue from "vue"
import api from "@/api/client"
import { handleError } from "@/utils"

const namespaced = true

const state = {
  clientProjects: [],
}

const mutations = {
  setClientProjects(state, clientProjects) {
    Vue.set(state, "clientProjects", clientProjects)
  },
}
const actions = {
  async getClientProjects({ commit }) {
    try {
      const response = await api.clients.all()
      commit("setClientProjects", response.data)
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
