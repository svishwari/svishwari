import Vue from "vue"
import Vuex from "vuex"
import createPersistedState from "vuex-persistedstate"

import users from "./modules/users"
import connections from "./modules/connections"

Vue.use(Vuex)

export default new Vuex.Store({
  modules: {
    users,
    connections,
  },

  strict: process.env.NODE_ENV !== "production",

  // Persist and rehydrates Vuex state between page reloads.
  // paths can be used to persist only specific states
  // ********TODO****************
  // Need to test it with API integration(incase of token change)
  // ****************************
  // https://github.com/robinvdvleuten/vuex-persistedstate
  plugins: [
    createPersistedState({
      paths: ["users"],
    }),
  ],
})
