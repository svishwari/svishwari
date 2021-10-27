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

  total: (state) => state.total,
}

const mutations = {
  SET_ALL(state, items) {
    items.notifications.forEach((item) => {
      Vue.set(state.items, item.id, item)
    })
  },

  SET_ONE(state, item) {
    Vue.set(state.items,item.id, item)
  },

  SET_TOTAL(state, item) {
    state.total = item
  },

  RESET_ALL(state) {
    Vue.set(state, "items", {})
  },
}

const actions = {
  async getAll({ commit }, batchDetails) {
    try {
      if (!batchDetails.isLazyLoad) {
        commit("RESET_ALL")
      }
      const response = await api.notifications.getNotifications(
        batchDetails.batchSize,
        batchDetails.batchNumber
      )
      // Replacing the special characters like (", ', <, >) with "
      response.data.notifications.forEach((notification) => {
        notification.description = notification.description.replace(
          />|<|"|'/g,
          /*eslint-disable */
          '"'
        )
      })
      commit("SET_TOTAL", response.data.total)
      commit("SET_ALL", response.data)
    } catch (error) {
      handleError(error)
      throw error
    }
  },

  async getById({ commit }, id) {
    try {
      const response = await api.notifications.getSingleNotification(id)
      commit("SET_ONE", response.data)
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
