import Vue from "vue"
import api from "@/api/client"
import { handleError } from "@/utils"

const namespaced = true

const state = {
  items: {},
}

const getters = {
  list: (state) => Object.values(state.items),
}

const mutations = {
  SET_ALL(state, items) {
    state.items = items
  },

  SET_ONE(state, item) {
    Vue.set(state.items, item.id, item)
  },
}

const actions = {
  async getAll({ commit }) {
    try {
      const response = await api.dataSources.all()
      commit("SET_ALL", response.data)
    } catch (error) {
      handleError(error)
      throw error
    }
  },

  async batchAdd({ commit }, dataSources) {
    try {
      const response = await api.dataSources.batchUpdate(dataSources)
      response.data.forEach((each) => {
        commit("SET_ONE", each)
      })
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
