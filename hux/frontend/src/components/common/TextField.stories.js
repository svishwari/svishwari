import TextField from "./TextField"

export default {
  component: TextField,

  title: "Components/Textbox",

  argTypes: {
    default: {
      control: {
        type: "text",
      },
    },
    variant: { control: "color" },
    click: { action: "clicked" },
  },

  args: {
    labelText: "Add Account ID",
    icon: "mdi-alert-circle-outline",
    placeholderText: "Account name",
  },

  parameters: {
    design: {
      type: "figma",
      url: "https://www.figma.com/file/nfrkMnYTxnjK5r2NTQqWb9/5.0-Release-06-21?node-id=1826%3A5",
    },
  },
}

const Template = (args, { argTypes }) => ({
  components: { TextField },
  props: Object.keys(argTypes),
  template: `
    <text-field v-bind="$props" v-on="$props">
        ${args.default}
    </text-field>
  `,
})

export const Textbox = Template.bind({})
