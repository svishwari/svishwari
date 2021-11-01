import { addDecorator } from "@storybook/vue"
import { withDesign } from "storybook-addon-designs"

// import vuetify configuration, theme and dependencies from the app
import vuetify from "../src/plugins/vuetify"

addDecorator(() => ({
  vuetify,
  withDesign,
  template: "<v-app><story/></v-app>",
}))
