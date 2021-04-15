const userStore = {
  namespace: true,
  state: {
    isLoading: false,
  },
  mutations: {
    LOADING: (state, data) => {
      state.isLoading = data
    },
  },
  actions: {},
  getters: {},
}
export default userStore
