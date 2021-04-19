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
  plugins: [
    createPersistedState({
      paths: ["user"],
    }),
  ],
})

export default store
