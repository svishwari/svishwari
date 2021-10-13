import { addDecorator } from "@storybook/vue"

// load in the vuetify configuration + theme for the app
import vuetify from "../src/plugins/vuetify"

// other dependencies
import "@mdi/font/css/materialdesignicons.css"

addDecorator(() => ({
  vuetify,
  template: "<v-app><story/></v-app>",
}))
