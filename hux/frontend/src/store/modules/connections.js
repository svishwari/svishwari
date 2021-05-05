import Vue from "vue"
import api from "@/api/client"

const state = {
  destinations: {},
}

const getters = {
  destinations: (state) => Object.values(state.destinations),
}

const mutations = {
  SET_ALL_DESTINATIONS(state, data) {
    data.forEach((item) => {
      Vue.set(state.destinations, item.id, item)
    })
  },
}

const actions = {
  async getAllDestinations({ commit }) {
    try {
      const response = await api.destinations.all()
      commit("SET_ALL_DESTINATIONS", response.data)
    } catch (error) {
      console.error(error)
    }
  },

  async addDestination({ commit }, destination) {
    try {
      const response = await api.destinations.update(
        destination.id,
        destination.auth_details
      )
      commit("SET_DESTINATIONS", response.data)
    } catch (error) {
      console.error(error)
    }
  },

  async validateDestination({ commit }, destination) {
    try {
      const response = await api.destinations.validate(
        destination.id,
        destination.auth_details
      )
      commit("SET_ALL_DESTINATIONS", response.data)
    } catch (error) {
      console.error(error)
    }
  },
}

export default {
  namespace: true,
  state,
  getters,
  mutations,
  actions,
}
