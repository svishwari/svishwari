import vuetify from "./addon-vuetify/custom"
import { addDecorator } from "@storybook/vue"
import "!style-loader!css-loader!sass-loader!../src/styles/variables.scss"

addDecorator(() => ({
  vuetify,
  template: "<v-app><story/></v-app>",
}))
