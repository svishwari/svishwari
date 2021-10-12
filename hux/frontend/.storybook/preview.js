import { addDecorator } from "@storybook/vue"

// import vuetify configuration, theme and dependencies from the app
import vuetify from "../src/plugins/vuetify"

addDecorator(() => ({
  vuetify,
  template: "<v-app><story/></v-app>",
}))
