import Vue from "vue"
import api from "@/api/client"
import { handleError } from "@/utils"

const namespaced = true

const state = {
  items: {},
}

const getters = {
  list: (state) => Object.values(state.items),

  single: (state) => (id) => state.items[id],

  dataFeeds: (state) => (id) => state.items[id]["dataFeeds"],

  dataFeedDetails: (state) => state.dataFeedsDetails,
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

  SET_DATA_FEEDS(state, data) {
    Vue.set(state.items[data.id], "dataFeeds", data.items)
  },

  SET_DATA_FEEDS_DETAILS(state, data) {
    Vue.set(state, "dataFeedsDetails", data)
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

  async getDataSource({ commit }, id) {
    try {
      const response = await api.dataSources.find(id)
      commit("SET_ONE", response.data)
    } catch (error) {
      handleError(error)
      throw error
    }
  },

  async batchUpdate({ commit }, dataSources) {
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

  async getDataFeeds({ commit }, data) {
    try {
      const response = await api.dataSources.dataFeeds(data.type)
      commit("SET_DATA_FEEDS", {
        items: response.data["datafeeds"],
        id: data.id,
      })
    } catch (error) {
      handleError(error)
      throw error
    }
  },

  async getDataFeedsDetails(
    { commit },
    { type, name, start_date = null, end_date = null, status = null }
  ) {
    try {
      const response = await api.dataSources.dataFeedsDetails(
        type,
        name,
        start_date,
        end_date,
        status
      )
      commit("SET_DATA_FEEDS_DETAILS", response.data)
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
