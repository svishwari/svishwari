import TextArea from "./TextArea"

export default {
  component: TextArea,

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
  components: { TextArea },
  props: Object.keys(argTypes),
  template: `
    <text-area v-bind="$props" v-on="$props">
        ${args.default}
    </text-area>
  `,
})

export const ATextArea = Template.bind({})
