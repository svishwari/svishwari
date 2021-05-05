import Vue from "vue"
import api from "@/api/client"

const namespaced = true

const state = {
  items: {},
}

const getters = {
  list: (state) => Object.values(state.items),
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
}

const actions = {
  async getAll({ commit }) {
    try {
      const response = await api.destinations.all()
      commit("SET_ALL", response.data)
    } catch (error) {
      console.error(error)
    }
  },

  async add({ commit }, destination) {
    try {
      const response = await api.destinations.update(
        destination.id,
        destination.auth_details
      )
      commit("SET_ONE", response.data)
    } catch (error) {
      console.error(error)
    }
  },

  async validate({ commit }, destination) {
    try {
      const response = await api.destinations.validate(
        destination.id,
        destination.auth_details
      )
      commit("SET_ONE", response.data)
    } catch (error) {
      console.error(error)
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
