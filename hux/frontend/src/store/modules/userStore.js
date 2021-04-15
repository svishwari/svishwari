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
      state.isLoading = data
    }
  },
  actions: { },
  getters: { },
};
export default userStore;
