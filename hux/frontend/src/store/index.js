import Vue from "vue"
import Vuex from "vuex"
import createPersistedState from "vuex-persistedstate"

import users from "@/store/modules/users"
import connections from "@/store/modules/connections"

Vue.use(Vuex)

const debug = process.env.NODE_ENV !== "production"

// TODO: test persisted state with integration incase of token changes
const persistedStores = ["users"]

export default new Vuex.Store({
  modules: {
    users,
    connections,
  },

  strict: debug,

  plugins: [
    createPersistedState({
      paths: persistedStores,
    }),
  ],
})
