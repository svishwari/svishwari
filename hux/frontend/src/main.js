import Vue from "vue"
import VueCompositionAPI from "@vue/composition-api"

import App from "@/App"
import filters from "@/filters"
import router from "./router"
import store from "./store"

// Styles
import "ngprogress/ngProgress.css"

// Layouts
import AppLayout from "@/layouts/AppLayout"
import DefaultLayout from "@/layouts/DefaultLayout"
import vuetify from "./plugins/vuetify"

// Layouts as usable components
Vue.component("app-layout", AppLayout)
Vue.component("default-layout", DefaultLayout)

Vue.use(VueCompositionAPI)

// Filters
Object.keys(filters).forEach((filterName) => {
  Vue.filter(filterName, filters[filterName])
})

Vue.config.productionTip = false

// API mock for local development only
if (process.env.NODE_ENV === "development") {
  const apiMock = require("./api/mock/server")
  apiMock.makeServer()
}

new Vue({
  router,
  store,
  vuetify,
  render: (h) => h(App),
}).$mount("#app")
