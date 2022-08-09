import radioButton from "./radioButton.vue"

export default {
  component: radioButton,

  title: "NewComponents/RadioButton",

  argTypes: {
    isDisabled: {
      control: { type: "boolean" },
    },
  },

  args: {
    isDisabled: false,
    labels: ["radio1", "radio2"],
  },

  parameters: {
    design: {
      type: "figma",
      url: "https://www.figma.com/file/nfrkMnYTxnjK5r2NTQqWb9/5.0-Release-06-21?node-id=1826%3A5",
    },
  },
}

const Template = (args, { argTypes }) => ({
  components: { radioButton },
  props: Object.keys(argTypes),
  template: `
    <radio-button v-bind="$props" v-on="$props" />
  `,
})

export const RadioButton = Template.bind({})
