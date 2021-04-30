import Vue from "vue"
import Vuex from "vuex"
import createPersistedState from "vuex-persistedstate"

import users from "./modules/users"
import connections from "./modules/connections"

Vue.use(Vuex)

const debug = process.env.NODE_ENV !== "production"

export default new Vuex.Store({
  modules: {
    users,
    connections,
  },

  strict: debug,

  plugins: [
    createPersistedState({
      // TODO: test persisted state with integration incase of token changes
      paths: ["users"],
    }),
  ],
})
