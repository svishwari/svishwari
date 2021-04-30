import Vue from "vue"

import App from "@/App"
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
Vue.component("default-Layout", DefaultLayout)

Vue.config.productionTip = false

Vue.filter("TitleCase", function (value) {
  return value
    .replace(/([A-Z])/g, (match) => ` ${match}`)
    .replace(/^./, (match) => match.toUpperCase())
    .trim()
})

if (process.env.NODE_ENV === "development") {
  makeServer()
}

new Vue({
  router,
  store,
  vuetify,
  render: (h) => h(App),
}).$mount("#app")
