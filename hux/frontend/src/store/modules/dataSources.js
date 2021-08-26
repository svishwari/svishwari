import Vue from "vue"
import api from "@/api/client"
import { handleError } from "@/utils"

const namespaced = true

const state = {
  items: {},

  data_feeds: [],
}

const getters = {
  list: (state) => Object.values(state.items),

  single: (state) => (id) => state.items[id],

  data_feeds: (state) => state.data_feeds,
}

const mutations = {
  SET_ALL(state, items) {
    items.forEach((item) => {
      Vue.set(state.items, item.id, item)
    })
  },

  SET_ONE(state, item) {
    Vue.set(state.items, item.id, item)
  },

  SET_DATA_FEEDS(state, items) {
    state.data_feeds = items
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

  async getDataFeeds({ commit }, id) {
    try {
      const response = await api.dataSources.find(id)
      commit("SET_DATA_FEEDS", response.data)
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
