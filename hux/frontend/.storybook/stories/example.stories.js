// Utilities
import { storyFactory } from '../util/helpers'
import { text, boolean } from '@storybook/addon-knobs'

export default { title: 'Button' }

function genComponent (name) {
  return {
    name,

    render (h) {
      return h('div', this.$slots.default)
    },
  }
}

const story = storyFactory({
  BaseBtn: genComponent('BaseBtn'),
  Button: genComponent('Button'),
})

export const asDefault = () => story({
  props: {
    normalButtonText: {
      default: text('Normal button text', 'Normal'),
    },
    primaryButtonText: {
      default: text('Primary button text', 'Primary'),
    },
    errorButtonText: {
      default: text('Error button text', 'Error'),
    },
    disabledButtonText: {
      default: text('Disable button text', 'Disabled'),
    },
  },
  template: `
  <template>
  <v-row
    align="center"
    justify="space-around"
  >
    <v-btn depressed>
      {{normalButtonText}}
    </v-btn>
    <v-btn
      depressed
      color="primary"
    >
    {{primaryButtonText}}
    </v-btn>
    <v-btn
      depressed
      color="error"
    >
    {{errorButtonText}}
    </v-btn>
    <v-btn
      depressed
      disabled
    >
    {{disabledButtonText}}
    </v-btn>
  </v-row>
</template>
  `,
})
