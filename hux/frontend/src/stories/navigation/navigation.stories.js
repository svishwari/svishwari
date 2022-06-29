import SideMenu from "./navigation.vue"
import sideBarItems from "./sideBarItems"

export default {
  component: SideMenu,

  title: "NewComponents/NAvigation",

  argTypes: {
    toggle: { control: "boolean" },
  },

  args: {
    sideBarItems: sideBarItems,
    toggle: false,
  },

  parameters: {
    design: {
      type: "figma",
      url: "https://www.figma.com/file/4qNDv9mcu1ZWZkZxO3fVpP/6.0-Release?node-id=1927%3A11902",
    },
  },
}

const Template = (args, { argTypes }) => ({
  components: { SideMenu },

  props: Object.keys(argTypes),

  methods: {},

  template: `
    <side-menu
      v-bind="$props" 
      v-on="$props"
    />
  `,
})

export const Navigation = Template.bind({})
