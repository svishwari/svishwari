import Vue from "vue"
import api from "@/api/client"
import { handleError } from "@/utils"
// import { getAllAudiences } from "@/api/resources/audiences"

const namespaced = true

const NEW_AUDIENCE = {
  name: "",
  engagements: [],
  attributeRules: [],
  destinations: [],
}

const state = {
  audiences: [],
  newAudience: NEW_AUDIENCE,
}

const getters = {
  list: (state) => state.audiences,
}

const mutations = {
  SET_ALL(state, items) {
    state.audiences = items
  },
  SET_AUDIENCE(state, data) {
    Vue.set(state.audiences, data.audienceId, data)
  },
}

const actions = {
  async getAll({ commit }) {
    try {
      const response = await api.audiences.all()
      commit("SET_ALL", response.data)
    } catch (error) {
      handleError(error)
      throw error
    }
  },
  async getAudienceById({ commit }, id) {
    try {
      const response = state.audiences.find(id)
      commit("SET_AUDIENCE", response.data)
    } catch (error) {
      /*
       *    to do item...
       */
    }
  },
  async add({ commit }, audience) {
    try {
      const response = await api.audiences.create(audience)
      commit("SET_AUDIENCE", response.data)
      return response.data
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
