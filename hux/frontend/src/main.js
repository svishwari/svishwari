import Vue from "vue"

import App from "@/App"
import filters from "@/filters"
import router from "./router"
import store from "./store"
import { makeServer } from "./api/mock/server"

// Styles
import "@mdi/font/css/materialdesignicons.css"
import "ngprogress/ngProgress.css"

// Layouts
import AppLayout from "@/layouts/AppLayout"
import DefaultLayout from "@/layouts/DefaultLayout"
import vuetify from "./plugins/vuetify"

// Layouts as usable components
Vue.component("app-layout", AppLayout)
Vue.component("default-layout", DefaultLayout)

// Filters
Object.keys(filters).forEach((filterName) => {
  Vue.filter(filterName, filters[filterName])
})

Vue.config.productionTip = false

if (process.env.NODE_ENV === "development") {
  makeServer()
}

new Vue({
  router,
  store,
  vuetify,
  render: (h) => h(App),
}).$mount("#app")
