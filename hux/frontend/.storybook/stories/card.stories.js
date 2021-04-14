// Utilities
import { storyFactory } from '../util/helpers'
import { text, boolean } from '@storybook/addon-knobs'

export default { title: 'Card' }

function genComponent (name) {
  return {
    name,

    render (h) {
      return h('div', this.$slots.default)
    },
  }
}

const story = storyFactory({
  Card: genComponent('Card'),
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
    <v-card class="mx-auto" max-width="255">
        <v-card-text>
            <v-row align="center" justify="center" style="margin-top: 15px;">
                <div class="logo">
                <v-img
                    src="https://cdn.vuetifyjs.com/images/cards/sun.png"
                    alt="Sunny image"
                    width="48">
                </v-img>
                </div>
            </v-row>
        </v-card-text>

        <v-row align="center" justify="center" style="margin-top: 10px;margin-top: 10px;
        text-align: center;
        margin-right: 33px;
        margin-left: 33px;">
            Salesforce Marketing Cloud
        </v-row>
    

        <v-list class="transparent" style="margin-left: 30px;margin-right:30px;margin-top:58px;">
            <v-list-item>
                <v-list-item-title> 
                    5 
                </v-list-item-title>

                <span class="divider" style="border: 0.5px solid #D0D0CE; transform: rotate(90deg);width: 70px;"> </span>

                <v-list-item-subtitle>
                    Yesterday
                </v-list-item-subtitle>
            </v-list-item>
        </v-list>

        <v-divider></v-divider>
  
    </v-card>
  `,
})
