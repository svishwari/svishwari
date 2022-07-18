import Toggle from "./Toggle.vue"

export default {
  component: Toggle,
  title: "NewComponents/Toggle",

  argTypes: {
    value: { control: "boolean" },
  },

  args: {
    value: true,
  },

  parameters: {
    design: {
      type: "figma",
      url: "https://www.figma.com/file/eCWUinup52AoHQw1FBVJkd/HDS-(Hux-Design-System)?node-id=9409%3A68520",
    },
  },
}

const Template = (args, { argTypes }) => ({
  components: { Toggle },
  props: Object.keys(argTypes),
  template: `
  <toggle v-bind="$props"/>`,
})

export const AToggle = Template.bind({})
