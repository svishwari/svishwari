import Error from "./Error.vue"
import AllIcons from "@/stories/icons/Icons"

export default {
  component: Error,

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
  components: { Error },
  props: Object.keys(argTypes),
  data() {
    return {
      openModal: false,
    }
  },
  template: `
    <error
        v-bind="$props"
        v-on="$props">
    </error>
    `,
})

export const ErrorScreen = Template.bind({})
