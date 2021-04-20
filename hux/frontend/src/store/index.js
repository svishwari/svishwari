import Vue from "vue"
import Vuex from "vuex"
import createPersistedState from "vuex-persistedstate"

/**
 * Module Based store imports
 */
import userStore from "./modules/userStore"

Vue.use(Vuex)
const debug = process.env.NODE_ENV !== "production"

const store = new Vuex.Store({
  modules: {
    user: userStore,
  },
  strict: debug,
  // Persist and rehydrates Vuex state between page reloads.
  // paths can be used to persist only specific states
  // ********TODO****************
  // Need to test it with API integration(incase of token change)
  // ****************************
  // https://github.com/robinvdvleuten/vuex-persistedstate
  plugins: [
    createPersistedState({
      paths: ["user"],
    }),
  ],
})

export default store
