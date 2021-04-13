// Utilities
import { storyFactory } from '../util/helpers'
import { text, boolean } from '@storybook/addon-knobs'

export default { title: 'BaseCard' }

function genComponent(name) {
  return {
    name,
    render(h) {
      return h('div', this.$slots.default)
    },
  }
}

const story = storyFactory({
  BaseBtn: genComponent('BaseBtn'),
  BaseCard: genComponent('BaseCard'),
})

export const asDefault = () => story({
  template: `
    <template>
      <v-row align="center" justify="space-around">
        <v-btn depressed>
          Normal
        </v-btn>
        <v-btn depressed color="primary" >
          Primary
        </v-btn>
        <v-btn depressed color="error" >
          Error
        </v-btn>
        <v-btn depressed disabled >
          Disabled
        </v-btn>
      </v-row>
    </template>
  `,
})
