export default {
  namespace: true,

  state: {
    userProfile: {
      firstName: null,
      lastName: null,
      token: null,
      idToken: null,
    },
  },

  mutations: {
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
  },

  actions: {
    setUserProfile: ({ commit }, userProfile) => {
      commit("setUserProfile", userProfile)
    },

    setUserToken: ({ commit }, token) => commit("setUserToken", token),
  },

  getters: {
    getFirstname: (state) => {
      return state.userProfile.firstName
    },

    getLastName: (state) => {
      return state.userProfile.lastName
    },
  },
}
