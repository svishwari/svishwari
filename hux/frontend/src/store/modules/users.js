import Vue from "vue"
import api from "@/api/client"
import { handleError, handleSuccess } from "@/utils"

const namespaced = true

const state = {
  userProfile: {
    firstName: null,
    lastName: null,
    email: null,
    token: null,
    idToken: null,
    bugsReported: [],
  },
}

const mutations = {
  setUserProfile(state, userProfile) {
    if (Object.keys(userProfile).length > 0) {
      state.userProfile.firstName = userProfile.userProfile.given_name
      state.userProfile.lastName = userProfile.userProfile.family_name
    } else {
      state.userProfile.firstName = null
      state.userProfile.lastName = null
    }
  },

  setUserToken(state, token) {
    if (Object.keys(token).length > 0) {
      state.userProfile.token = token.accessToken.value
      state.userProfile.idToken = token.idToken.value
    } else {
      state.userProfile.token = null
      state.userProfile.idToken = null
    }
  },

  setApplicationUserProfile(state, userProfile) {
    Vue.set(state, "userProfile", { ...state.userProfile, ...userProfile })
  },
}

const actions = {
  setUserProfile: ({ commit }, userProfile) => {
    commit("setUserProfile", userProfile)
  },

  setUserToken: ({ commit }, token) => commit("setUserToken", token),

  async getUserProfile({ commit }) {
    try {
      const response = await api.users.fetchProfile()
      commit("setApplicationUserProfile", response.data)
    } catch (error) {
      handleError(error)
      throw error
    }
  },

  async markFavorite({ dispatch }, { id, type }) {
    try {
      await api.users.markFavorite(id, type)
      dispatch("getUserProfile")
    } catch (error) {
      handleError(error)
      throw error
    }
  },

  async clearFavorite({ dispatch }, { id, type }) {
    try {
      await api.users.clearFavorite(id, type)
      dispatch("getUserProfile")
    } catch (error) {
      handleError(error)
      throw error
    }
  },

  async contactUs(_, data) {
    try {
      let res = await api.users.contactUs(data)
      if (res) {
        handleSuccess(
          `Bug Submitted Successfully with JIRA ID: ${res.data.key}`,
          res.status
        )
      }
    } catch (error) {
      handleError(error)
      throw error
    }
  },
}

const getters = {
  favorites: (state) => {
    return state.userProfile.favorites
  },

  getFirstname: (state) => {
    return state.userProfile.firstName
  },

  getLastName: (state) => {
    return state.userProfile.lastName
  },

  getEmailAddress: (state) => state.userProfile.email,
}
export default {
  namespaced,
  state,
  getters,
  mutations,
  actions,
}
