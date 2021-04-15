import Vue from "vue"
import Vuex from "vuex"

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
  plugins: debug ? [] : [],
})

export default store
