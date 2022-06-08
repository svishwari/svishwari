import Pill from "./Pill.vue"

export default {
  component: Pill,
  title: "Design System/Pills",
  argTypes: {
    label: { control: { type: "text" } },
    removable: { control: { type: "boolean" } },
    hover: { control: { type: "text" } },
    dropdown: { control: { type: "boolean" } },
    color: {
      options: [
        "white-base",
        "black-lighten7",
        "black-lighten1",
        "black-lighten8",
        "black-lighten5",
        "black-lighten6",
        "black-base",
        "primary-lighten7",
        "primary-base",
        "success-darken1",
        "error-lighten1",
        "warning-lighten1",
        "yellow-lighten3",
        "primary-darken7",
        "primary-lighten4",
        "primary-lighten6",
        "yellow-lighten2",
        "secondary-darken1",
        "secondary-lighten1",
        "primary-darken3",
        "secondary-lighten4",
        "primary-darken6",
        "yellow-darken1",
        "primary-darken5",
        "secondary-lighten2",
      ],
      control: {
        type: "select",
        labels: {
          "white-base": "White",
          "black-lighten7": "Light background",
          "black-lighten1": "Grey 1",
          "black-lighten8": "Grey 2",
          "black-lighten5": "Grey 3",
          "black-lighten6": "Grey 4",
          "black-base": "Grey 5 (Black)",
          "primary-lighten7": "Blue 1 (Active)",
          "primary-base": "Blue 2 (Selected)",
          "success-darken1": "Green",
          "error-lighten1": "Red",
          "warning-lighten1": "Orange",
          "yellow-lighten3": "Yellow",
          "primary-darken7": "Deloitte blue 4",
          "primary-lighten4": "Deloitte blue 1",
          "primary-lighten6": "Deloitte blue 3",
          "yellow-lighten2": "Deloitte green 1",
          "secondary-darken1": "Deloitte teal 6",
          "secondary-lighten1": "Deloitte teal 2",
          "primary-darken3": "Deloitte blue 6",
          "secondary-lighten4": "Deloitte blue 2",
          "primary-darken6": "Humanity",
          "yellow-darken1": "Transparency",
          "primary-darken5": "Capability",
          "secondary-lighten2": "Reliability",
        },
      },
    },
    darkText: { control: { type: "boolean" } },
  },
  args: {
    label: "Pill",
    removable: false,
    dropdown: false,
    color: "primary-base",
  },
  parameters: {
    design: {
      type: "figma",
      url: "https://www.figma.com/file/4qNDv9mcu1ZWZkZxO3fVpP/6.0-Release?node-id=11331%3A256774",
    },
  },
}

const Template = (args, { argTypes }) => ({
  components: { Pill },
  props: Object.keys(argTypes),
  data() {
    return {}
  },
  template: `
    <div>
      <pill v-bind="$props" />
    </div>`,
})

export const Default = Template.bind({})
