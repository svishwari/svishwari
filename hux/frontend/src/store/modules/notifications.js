import Vue from "vue"
import api from "@/api/client"
import { handleError } from "@/utils"

const namespaced = true

const state = {
  items: {},
  users: {},
  latest5: {},
  total: 0,
  seenNotifications: false,
  error_alerts: {},
}

const getters = {
  list: (state) => Object.values(state.items),

  latest5: (state) => Object.values(state.latest5),

  userList: (state) => Object.values(state.users),

  single: (state) => (id) => state.items[id],

  total: (state) => state.total,

  seenNotifications: (state) => state.seenNotifications,

  error_alerts: (state) => state.error_alerts,
}

const mutations = {
  SET_ALL(state, items) {
    items.notifications.forEach((item) => {
      Vue.set(state.items, item.id, item)
    })
  },
  SET_ALL_USERS(state, items) {
    Vue.set(state, "users", items)
  },

  SET_ONE(state, item) {
    Vue.set(state.items, item.id, item)
  },

  SET_TOTAL(state, item) {
    Vue.set(state, "total", item)
  },

  SET_SEEN_NOTIFICATIONS(state, item) {
    Vue.set(state, "seenNotifications", item)
  },

  RESET_ALL(state) {
    Vue.set(state, "items", {})
  },

  SET_LATEST(state, items) {
    items.notifications.forEach((item) => {
      Vue.set(state.latest5, item.id, item)
    })
  },

  SET_ERROR_ALERTS(state, data) {
    Vue.set(state, "error_alerts", data)
  },
}

const actions = {
  async getAll({ commit }, batchDetails) {
    try {
      if (!batchDetails.isLazyLoad) {
        commit("RESET_ALL")
      }
      const response = await api.notifications.getNotifications(batchDetails)
      // Replacing the special characters like (", ', <, >) with "
      response.data.notifications.forEach((notification) => {
        notification.description = notification.description.replace(
          />|<|"|'/g,
          /*eslint-disable */
          '"'
        )
      })
      if (batchDetails.batchSize === 5) {
        commit("SET_LATEST", response.data)
      } else {
        commit("SET_TOTAL", response.data.total)
        commit("SET_ALL", response.data)
      }
      commit("SET_SEEN_NOTIFICATIONS", response.data.seen_notifications)
      commit("SET_ERROR_ALERTS", response.data.error_alerts)
    } catch (error) {
      handleError(error)
      throw error
    }
  },

  async getById({ commit }, id) {
    try {
      const response = await api.notifications.find(id)
      commit("SET_ONE", response.data)
    } catch (error) {
      handleError(error)
      throw error
    }
  },
  async getAllUsers({ commit }) {
    try {
      const response = await api.notifications.getAllUsers()
      commit("SET_ALL_USERS", response.data)
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
