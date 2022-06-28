import Banner from "./Banner.vue"

export default {
  component: Banner,

  title: "NewComponents/Banners",

  argTypes: {
    label: { control: { type: "text" } },
    type: {
      options: ["Checkmark", "Guide", "Error & Warning", "Error"],
      control: { type: "select" },
    },
    size: {
      options: ["small", "large"],
      control: { type: "select" },
    },
    height: { control: { type: "number" } },
    width: { control: { type: "number" } },
    outlined: {
      control: { type: "boolean" },
    },
  },

  args: {
    label: "This is a banner.",
  },

  parameters: {
    design: {
      type: "figma",
      url: "https://www.figma.com/file/nfrkMnYTxnjK5r2NTQqWb9/5.0-Release-06-21?node-id=1826%3A5",
    },
  },
}

const Template = (args, { argTypes }) => ({
  components: { Banner },
  props: Object.keys(argTypes),
  template: `
    <banner v-bind="$props" v-on="$props">
      ${args.default}
    </banner>
  `,
})

export const Default = Template.bind({})
