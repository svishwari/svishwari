import Vue from "vue"
import Vuex from "vuex"
import createPersistedState from "vuex-persistedstate"

import audiences from "@/store/modules/audiences"
import dataSources from "@/store/modules/dataSources"
import destinations from "@/store/modules/destinations"
import engagements from "@/store/modules/engagements"
import models from "@/store/modules/models"
import users from "@/store/modules/users"

Vue.use(Vuex)

const debug = process.env.NODE_ENV !== "production"

// TODO: test persisted state with integration incase of token changes
const persistedStores = ["users"]

export default new Vuex.Store({
  modules: {
    audiences,
    dataSources,
    destinations,
    engagements,
    models,
    users,
  },

  strict: debug,

  plugins: [
    createPersistedState({
      paths: persistedStores,
    }),
  ],
})
