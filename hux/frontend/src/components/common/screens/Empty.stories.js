import HuxEmpty from "./Empty.vue"
import HuxButton from "../huxButton.vue"
import AllIcons from "@/stories/icons/Icons"
import { action } from "@storybook/addon-actions"

export default {
  component: HuxEmpty,

  title: "Components/Screens",

  argTypes: {
    iconType: {
      options: AllIcons,
      control: {
        type: "select",
      },
    },
    iconSize: { control: { type: "number" } },
    title: { control: { type: "text" } },
    button: { table: { disable: true } },
  },

  args: {
    title: "No data sources to show",
    subtitle:
      "The list of data sources will appear here once they have been added.",
    iconType: "destinations-null",
    iconSize: 50,
  },

  parameters: {
    design: {
      type: "figma",
      url: "",
    },
  },
}

const Template = (args, { argTypes }) => ({
  components: { HuxEmpty, HuxButton },
  props: Object.keys(argTypes),
  methods: { toggleDrawer: action("clicked") },
  data() {
    return {
      openModal: false,
    }
  },
  template: `
    <hux-empty
        v-bind="$props"
        v-on="$props">
        <template #button>
            <hux-button
                variant="primary"
                is-tile
                width="224"
                height="40"
                class="text-button my-4"
                @click="toggleDrawer()">
                Request a data sources
            </hux-button>
        </template>
    </hux-empty>
    `,
})

export const EmptyScreen = Template.bind({})
