const userStore = {
  namespace: true,
  state: {
    isLoading: false,
    userName: {
      firstName: null,
      lastName: null,
    }
  },
  mutations: {
    LOADING: (state, data) => {
      state.isLoading = data;
    },
    SET_USER_NAME: (state, data) => {
      state.userName.firstName = data.firstName;
      state.userName.lastName = data.lastName;
    },
  },
  actions: { },
  getters: { },
};
export default userStore;
