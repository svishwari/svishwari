const userStore = {
  namespace: true,
  state: {
    isLoading: false,
    userProfile: {
      firstName: null,
      lastName: null,
      token: null,
      idToken: null,
    }
  },
  mutations: {
    LOADING: (state, data) => {
      state.isLoading = data
    },
    setUserProfile(state, userProfile) {
      state.userProfile.firstName = userProfile.userProfile.firstName;
      state.userProfile.lastName = userProfile.userProfile.lastName;
    },
    setUserToken(state, token) {
      state.userProfile.token = token.accessToken.value;
      state.userProfile.idToken = token.idToken.value;
    }
  },
  actions: {
    setUserProfile: ({ commit }, userProfile) => commit('setUserProfile', userProfile),
    setUserToken: ({ commit }, token) => commit('setUserToken', token)
   },
  getters: {
    getFirstname: state => {
      return state.userProfile.firstName
    },
    getLastName: state => {
      return state.userProfile.lastName
    }
   },
};
export default userStore;
