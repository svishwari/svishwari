// Utilities
import { storyFactory } from '../util/helpers'
import { text, boolean } from '@storybook/addon-knobs'

export default { title: 'Text Field' }

function genComponent (name) {
  return {
    name,

    render (h) {
      return h('div', this.$slots.default)
    },
  }
}

const story = storyFactory({
  TextField: genComponent('TextField'),
})

export const asDefault = () => story({
  props: {
    labelText: {
      default: text('Label text', 'Add Account ID'),
    },
    placeholderText: {
      default: text('Placeholder text', 'Account name'),
    },
  },
  template: `
            <v-form>
                <v-container>
                    <v-row>
                        <v-col cols="12" sm="6">
                            <label>{{ labelText }}</label>
                            <v-text-field v-model="placeholderText" single-line outlined> </v-text-field>
                        </v-col>
                    </v-row>
                </v-container>
            </v-form>
            `,
})
