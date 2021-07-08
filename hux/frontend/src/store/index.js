import Vue from "vue"
import Vuex from "vuex"
import createPersistedState from "vuex-persistedstate"

import audiences from "@/store/modules/audiences"
import customers from "@/store/modules/customers"
import dataSources from "@/store/modules/dataSources"
import destinations from "@/store/modules/destinations"
import engagements from "@/store/modules/engagements"
import identity from "@/store/modules/identity"
import models from "@/store/modules/models"
import users from "@/store/modules/users"
import notification from "@/store/modules/notification"

Vue.use(Vuex)

const debug = process.env.NODE_ENV !== "production"

// TODO: test persisted state with integration incase of token changes
const persistedStores = ["users"]

export default new Vuex.Store({
  modules: {
    audiences,
    customers,
    dataSources,
    destinations,
    engagements,
    identity,
    models,
    users,
    notification
  },

  strict: debug,

  plugins: [
    createPersistedState({
      paths: persistedStores,
    }),
  ],
})
