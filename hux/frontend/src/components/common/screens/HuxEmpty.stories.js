import HuxEmpty from "./HuxEmpty.vue"
import HuxButton from "../huxButton.vue"
import AllIcons from "@/stories/icons/Icons"

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
  },

  args: {
    title: "No data sources to show",
    subtitle: "The list of data sources will appear here once they have been added.",
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
