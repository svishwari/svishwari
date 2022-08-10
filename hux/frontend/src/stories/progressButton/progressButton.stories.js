import ProgressButton from "./progressButton.vue"

export default {
  component: ProgressButton,

  title: "NewComponents/Button",

  argTypes: {
    variant: {
      type: "select",
      options: ["validate", "progressing", "success", "error"],
    },
  },

  args: {
    variant: "validate",
  },

  parameters: {
    design: {
      type: "figma",
      url: "https://www.figma.com/file/nfrkMnYTxnjK5r2NTQqWb9/5.0-Release-06-21?node-id=1826%3A5",
    },
  },
}

const Template = (args, { argTypes }) => ({
  components: { ProgressButton },
  props: Object.keys(argTypes),
  template: `
    <progress-button v-bind="$props" v-on="$props"/>
  `,
})

export const AProgressButton = Template.bind({})
