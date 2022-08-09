import Page2 from "./Page2.vue"

export default {
  component: Page2,
  title: "NewComponents/Page2",

  argTypes: {
    maxWidth: { control: "text" },
    padding: { control: "text" },
    errorState: { control: "boolean" },
    emptyState: { control: "boolean" },
  },

  args: {
    maxWidth: "auto",
    padding: "auto",
    errorState: true,
    emptyState: false,
  },

  parameters: {
    design: {
      type: "figma",
      url: "https://www.figma.com/file/eCWUinup52AoHQw1FBVJkd/HDS-(Hux-Design-System)?node-id=9409%3A68520",
    },
  },
}

const Template = (args, { argTypes }) => ({
  components: { Page2 },
  props: Object.keys(argTypes),
  template: `
  <page2 v-bind="$props" />`,
})

export const newPage = Template.bind({})
