import colors from "./colors"
import allColors from "./allColors"

const BasicTemplate = (args, { argTypes }) => ({
  props: Object.keys(argTypes),
  methods: {
    getClass(color) {
      return `var(--v-${color})`
    },
  },
  template: `<div>
                <v-card
                      width="220"
                      class="ml-5 mb-4"
                      elevation="1"
                      shaped
                    >
                      <div
                        style="height: 112px; width: 100%"
                        class="d-flex"
                        :style="{
                            backgroundColor: getClass($props.color),
                          border: 'solid 1px #e2eaec',
                        }"
                      ></div>
                      <v-card-text>
                        <v-row
                          class="mx-0 mt-0 text-subtitle-2 d-flex flex-column"
                        >
                          <span class="text-h5">CSS class:</span>
                          <span>{{getClass($props.color)}}</span>
                        </v-row>
                      </v-card-text>
                    </v-card></div>`,
})

const TemplateAll = (args) => ({
  props: Object.keys(args),
  methods: {
    getClass(color) {
      return `var(--v-${color.class})`
    },
  },
  template: `
  <div>
      <v-item-group mandatory>
      <v-sheet class="overflow-y-auto" tile>
      <v-item v-for="color in Object.keys($props.colors)" :key="color">
      <template v-slot:default="{ active, toggle }">
            <v-sheet
              :color="
                active
                    ? 'backgroundMed'
                  : undefined
              "
              tile
              @click="toggle"
            >
              <div class="transition-swing text-uppercase text-h3 pa-5"> {{ color}} colors
              </div>
              <v-expand-transition>
                <v-responsive>
                  <div class="d-flex flex-wrap mt-5">
                    <v-card
                      v-for="indColor in colors[color]"
                      :key="indColor.hex"
                      width="220"
                      class="ml-5 mb-4"
                      elevation="1"
                      shaped
                    >
                    
                      <div
                        style="height: 112px; width: 100%"
                        class="d-flex"
                        :style="{
                            backgroundColor: getClass(indColor),
                          border: 'solid 1px #e2eaec',
                        }"
                      ></div>
                      <v-card-title class="text-caption">{{
                        indColor.title
                      }}</v-card-title>
                      <v-card-text>
                        <v-row
                          class="mx-0 mt-0 text-subtitle-2 d-flex flex-column"
                        >
                          <span class="text-h5">CSS class:</span>
                          <span>{{getClass(indColor)}}</span>
                          <span class="hover">
                            {{ indColor.hex }}
                          </span>
                        </v-row>
                      </v-card-text>
                    </v-card>
                  </div>
                </v-responsive>
              </v-expand-transition>
            </v-sheet>
          </template>
      </v-item>
      </v-sheet>
    </v-item-group>
  </div>`,
})

export default {
  title: "Design System/Colors",
  decorators: [() => ({ template: "<story/>" })],

  argTypes: {
    color: {
      options: allColors,
      control: {
        type: "select",
        labels: {
          "white-base": "White",
          "black-lighten7": "Light background",
          "black-lighten1": "Grey 1",
          "black-lighten8": "Grey 2",
          "black-lighten5": "Grey 3",
          "black-lighten6": "Grey 4",
          "black-base": "Grey 5 (Black)",
          "primary-lighten7": "Blue 1 (Active)",
          "primary-base": "Blue 2 (Selected)",
          "success-darken1": "Green",
          "error-lighten1": "Red",
          "warning-lighten1": "Orange",
          "yellow-lighten3": "Yellow",
          "primary-darken7": "Deloitte blue 4",
          "primary-lighten4": "Deloitte blue 1",
          "primary-lighten6": "Deloitte blue 3",
          "yellow-lighten2": "Deloitte green 1",
          "secondary-darken1": "Deloitte teal 6",
          "secondary-lighten1": "Deloitte teal 2",
          "primary-darken3": "Deloitte blue 6",
          "secondary-lighten4": "Deloitte blue 2",
          "primary-darken6": "Humanity",
          "yellow-darken1": "Transparency",
          "primary-darken5": "Capability",
          "secondary-lighten2": "Reliability",
        },
      },
    },
  },

  args: {},
}

export const Default = BasicTemplate.bind({})

export const List = TemplateAll.bind({})
List.args = { colors: colors }
