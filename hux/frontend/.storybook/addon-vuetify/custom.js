import Vue from "vue"
import Vuetify from "vuetify" // loads all components
import "vuetify/dist/vuetify.min.css" // all the css for components
import "@mdi/font/css/materialdesignicons.min.css" // all the css for components

import lightTheme from "../../src/plugins/theme"
const config = {
  theme: {
    options: { customProperties: true },
    dark: false,
    themes: {
      light: lightTheme,
    },
  },
}

Vue.use(Vuetify)

export default new Vuetify(config)
