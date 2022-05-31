import OptionsBar from "../components/common/OptionsBar.vue"

export default {
  component: OptionsBar,
  title: "NewComponents/OptionsBar",

  argTypes: {
    height: { control: "number" },
    buttonText: { control: "text" },
    numicons: { control: "number" },
    searchBar: { control: "boolean" },
    padding: { table: { disable: "true" } },
    heightChanges: { table: { disable: "true" } },
  },

  args: {
    buttonText: "Button",
    icons: ["add", "add", "add"],
    searchBar: "true",
  },
}

const Template = (args, { argTypes }) => ({
  components: { OptionsBar },
  props: Object.keys(argTypes),
  template: `
  <options-bar v-bind="$props"/>`,
})

export const optionsBar = Template.bind({})
