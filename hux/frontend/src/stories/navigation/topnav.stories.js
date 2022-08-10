import TopNav from "./NavBar.vue"

export default {
  component: TopNav,

  title: "NewComponents/Navigation",

  argTypes: {},

  args: {},

  parameters: {
    design: {
      type: "figma",
      url: "https://www.figma.com/file/4qNDv9mcu1ZWZkZxO3fVpP/6.0-Release?node-id=1927%3A11902",
    },
  },
}

const Template = (args, { argTypes }) => ({
  components: { TopNav },

  props: Object.keys(argTypes),

  methods: {},

  template: `
    <top-nav
      v-bind="$props" 
      v-on="$props"
    />
  `,
})

export const TopNavigation = Template.bind({})
