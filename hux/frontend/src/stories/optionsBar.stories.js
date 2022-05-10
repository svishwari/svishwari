import OptionsBar from "../components/common/OptionsBar.vue"

export default {
  component: OptionsBar,
  title: "NewComponents/OptionsBar",

  argTypes: {
    height: { control: 'number' },
    buttonText: { control: 'text' },
    numicons: { control: 'number' },
    icons: { control: 'text' },
    searchBar: { control: 'boolean' },
  },

  args: {
    buttonText: "Main CTA",
    icons: ["add", "add", "add"],
    searchBar: "true",
  }
}

const Template = (args, { argTypes }) => ({
  components: { OptionsBar },
  props: Object.keys(argTypes),
  template: `
  <options-bar v-bind="$props"/>`,
})

export const OptionBar = Template.bind({})
