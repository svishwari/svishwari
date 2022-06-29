import SearchBar from "./SearchBar.vue"

export default {
  component: SearchBar,
  title: "Design System/Search",
  argTypes: {
    placeholderText: { control: { type: "text" } },
  },
}

const Template = (args, { argTypes }) => ({
  components: { SearchBar },
  props: Object.keys(argTypes),
  template: `
    <search-bar v-bind="$props" />
  `,
})

export const searchBar = Template.bind({})
