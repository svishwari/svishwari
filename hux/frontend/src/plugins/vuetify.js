import Vue from "vue"
import Vuetify from "vuetify/lib/framework"
import lightTheme from "./theme"

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
