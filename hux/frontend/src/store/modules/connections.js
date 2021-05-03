import Vue from "vue"
// import { getAllDestinations } from "@/api/resources/destinations"

import axios from "axios"

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
      const response = await axios.get(
        "http://localhost:5000/api/v1/destinations"
      )
      commit("SET_ALL_DESTINATIONS", response.data)
    } catch (error) {
      console.error(error)
    }
  },
}

export default {
  state,
  getters,
  mutations,
  actions,
}
