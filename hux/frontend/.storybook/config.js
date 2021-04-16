// Imports
import { configure, addDecorator } from "@storybook/vue"
import { withA11y } from "@storybook/addon-a11y"
import { withKnobs } from "@storybook/addon-knobs"
import { withTemplate } from "~storybook/addon-show-vue-markup"
import { withVuetify } from "~storybook/addon-vuetify"
import vuetifyConfig from "../src/plugins/vuetify"

addDecorator(() => ({
  vuetify: vuetifyConfig,
  template: `
    <v-app>
      <v-main>
        <story/>
      </v-main>
    </v-app>
  `,
}))

addDecorator(withA11y)
addDecorator(withKnobs)
addDecorator(withTemplate)
addDecorator(withVuetify)

const stories = require.context("./stories", true, /\.stories\.js$/)
configure(stories, module)
