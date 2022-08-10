import TextField from "./TextField"

export default {
  component: TextField,

  title: "NewComponents/TextField",

  argTypes: {
    default: {
      control: {
        type: "text",
      },
    },
    variant: { control: "color" },
    click: { table: { disable: true } },
  },

  args: {
    labelText: "Engagement name",
    icon: "mdi-alert-circle-outline",
    placeholderText: "Name of Engagement",
  },

  parameters: {
    design: {
      type: "figma",
      url: "https://www.figma.com/file/4qNDv9mcu1ZWZkZxO3fVpP/6.0-Release?node-id=1840%3A3573",
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

export const ATextField = Template.bind({})
