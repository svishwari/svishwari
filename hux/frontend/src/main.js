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

//Mixin
Vue.mixin({
  methods: {
    sortByKey: function (array, key, order = "desc") {
      return array.sort(function (a, b) {
        var x = a[key]
        var y = b[key]
        if (order == "desc") {
          return x > y ? -1 : x < y ? 1 : 0
        } else {
          return x < y ? -1 : x > y ? 1 : 0
        }
      })
    },
  },
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
