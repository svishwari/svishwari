import checkBox from "./checkBox.vue"

export default {
  component: checkBox,

  title: "NewComponents/CheckBox",

  argTypes: {
    isDisabled: {
      control: { type: "boolean" },
    },
  },

  args: {
    isDisabled: false,
  },

  parameters: {
    design: {
      type: "figma",
      url: "https://www.figma.com/file/nfrkMnYTxnjK5r2NTQqWb9/5.0-Release-06-21?node-id=1826%3A5",
    },
  },
}

const Template = (args, { argTypes }) => ({
  components: { checkBox },
  props: Object.keys(argTypes),
  template: `
    <check-box v-bind="$props" v-on="$props" />
  `,
})

export const CheckBox = Template.bind({})
