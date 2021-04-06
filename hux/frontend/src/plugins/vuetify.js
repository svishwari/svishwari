import Vue from "vue";
import Vuetify from "vuetify/lib/framework";

Vue.use(Vuetify);

export default new Vuetify({
  theme: {
    themes: {
      light: {
        primary: "#005587",
        secondary: "#00A3E0",
        accent: "#82B1FF",
        error: "#DA291C",
        info: "#0076A8",
        success: "#009A44",
        warning: "#FFCD00",
      },
    },
  },
});
