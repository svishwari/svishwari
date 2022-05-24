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
    pii_access: false,
    alerts: {},
    demo_config: {},
  },
  users: [],
  requestedUsers: [],
  tickets: [],
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

  setApplicationAllUsers(state, users) {
    Vue.set(state, "users", users)
  },

  setTickets(state, tickets) {
    Vue.set(state, "tickets", tickets)
  },

  setAllRequestedUsers(state, requestedUsers) {
    Vue.set(state, "requestedUsers", requestedUsers)
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

  async getUsers({ commit }) {
    try {
      const response = await api.users.all()
      commit("setApplicationAllUsers", response.data)
    } catch (error) {
      handleError(error)
      throw error
    }
  },

  async getTickets({ commit }) {
    try {
      const response = await api.users.tickets()
      commit("setTickets", response.data)
    } catch (error) {
      handleError(error)
      throw error
    }
  },

  async getRequestedUsers({ commit }) {
    try {
      const response = await api.users.getRequestedUsers()
      commit("setAllRequestedUsers", response.data)
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

  async updateUser(_, payload) {
    try {
      const result = await api.users.batchUpdate(payload)
      return result
    } catch (error) {
      handleError(error)
      throw error
    }
  },

  async requestTeamMember(_, payload) {
    try {
      const result = await api.users.requestTeamMember(payload)
      if (result && result.status == 201) {
        handleSuccess(result.data.summary, result.status)
      }
      return result
    } catch (error) {
      handleError(error)
      throw error
    }
  },
  async updateUserPreferences({ commit }, payload) {
    try {
      const response = await api.users.updatePreferences(payload)
      if (response) {
        handleSuccess(
          "Alerts Configuration Saved Successfully",
          response.status
        )
      }
      commit("setApplicationUserProfile", response.data)
    } catch (error) {
      handleError(error)
      throw error
    }
  },

  async updateDemoConfig({ commit }, payload) {
    try {
      const response = await api.users.updateDemoConfig({
        demo_config: payload,
      })
      if (response) {
        handleSuccess("Demo Configuration Saved Successfully", response.status)
      }
      commit("setApplicationUserProfile", response.data)
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

  getPiiAccess: (state) => state.userProfile.pii_access,

  getUsers: (state) => state.users,

  getCurrentUserRole: (state) => state.userProfile.role,

  getRequestedUsers: (state) => state.requestedUsers,

  getAllTickets: (state) => state.tickets,

  getUserAlerts: (state) => state.userProfile.alerts,

  getDemoConfiguration: (state) => state.userProfile.demo_config,
}
export default {
  namespaced,
  state,
  getters,
  mutations,
  actions,
}
