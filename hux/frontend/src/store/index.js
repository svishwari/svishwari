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
import clients from "@/store/modules/clients"
import notifications from "@/store/modules/notifications"
import alerts from "@/store/modules/alerts"
import configuration from "@/store/modules/configurations"
import application from "@/store/modules/application"
import emailDeliverability from "@/store/modules/emailDeliverability"
import trustId from "@/store/modules/trustId"

Vue.use(Vuex)

const debug = process.env.NODE_ENV !== "production"

// TODO: test persisted state with integration incase of token changes
const persistedStores = ["users"]

export default new Vuex.Store({
  modules: {
    audiences,
    alerts,
    customers,
    dataSources,
    destinations,
    engagements,
    identity,
    models,
    users,
    clients,
    notifications,
    configuration,
    application,
    emailDeliverability,
    trustId,
  },

  strict: debug,

  plugins: [
    createPersistedState({
      paths: persistedStores,
    }),
  ],
})
