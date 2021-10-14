import Vue from "vue"
import Vuetify from "vuetify"
import lightTheme from "./theme"

// vuetify dependencies: mdi icon-font
import "@mdi/font/css/materialdesignicons.css"

Vue.use(Vuetify)

export default new Vuetify({
  theme: {
    options: { customProperties: true },
    dark: false,
    themes: {
      light: lightTheme,
    },
  },
})
