import colors from "./colors"
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
      options: [
        "black-lighten2",
        "black-lighten3",
        "primary-lighten2",
        "primary-lighten1",
        "white-base",
        "yellow-base",
        "yellow-lighten1",
        "primary-lighten5",
        "primary-darken3",
        "black-lighten1",
        "primary-lighten3",
        "primary-darken2",
        "black-base",
        "black-lighten4",
        "warning-base",
        "success-base",
        "primary-lighten6",
        "secondary-lighten1",
        "success-lighten3",
        "info-base",
        "primary-lighten4",
        "primary-darken1",
        "success-lighten2",
        "secondary-darken1",
        "secondary-darken2",
        "error-base",
        "primary-base",
        "primary-lighten9",
      ],
      control: {
        type: "select",
        labels: {
          "black-lighten2": "Lines & Borders (Light)",
          "black-lighten3": "Lines (Heavy)",
          "primary-lighten2": "Background (Med)",
          "primary-lighten1": "Background (Light)",
          "white-base": "White",
          "yellow-base": "Yellow",
          "yellow-lighten1": "5% Yellow",
          "primary-lighten5": "Map Blue",
          "primary-darken3": "Blue",
          "black-lighten1": "Inactive Button Background color",
          "primary-lighten3": "Pills",
          "primary-darken2": "Dark Blue (Blue 5) Clickable",
          "black-base": "Dark - D",
          "black-lighten4": "Light Gray - D",
          "error-base": "Error",
          "warning-base": "Warning",
          "primary-lighten6": "Blue D (Active)",
          "secondary-lighten1": "Light Teal D",
          "success-lighten3": "Light Green D",
          "success-base": "Green D",
          "yellow-darken1": "Mustard Yellow D",
          "primary-lighten4": "Light Blue D",
          "primary-darken1": "Med Blue D",
          "success-lighten2": "Teal D",
          "secondary-darken1": "Teal 6 D",
          "secondary-darken2": "Teal 7 D",
          "primary-base": "Chart 1",
          "primary-lighten9": "Chart 3",
        },
      },
    },
  },

  args: {},
}

export const Default = BasicTemplate.bind({})

export const List = TemplateAll.bind({})
List.args = { colors: colors }
