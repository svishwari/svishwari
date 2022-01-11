import HuxStartDate from "./HuxStartDate.vue"

export default {
  component: HuxStartDate,
  title: "Components/DatePicker",
  argTypes: {
    selected: {
      control: { type: "array" },
    },
    label: {
      control: { type: "text" },
    },
    isOffsetX: {
      control: { type: "boolean" },
    },
    isOffsetY: {
      control: { type: "boolean" },
    },
    isOpenOnHover: {
      control: { type: "boolean" },
    },
    transition: {
      options: ["scale-transition", "slide-x-transition", "slide-y-transition"],
      control: { type: "select" },
    },
  },
  args: {
    selected: [],
    label: "Select Option",
    isOffsetX: false,
    isOffsetY: true,
    isOpenOnHover: false,
    transition: "scale-transition",
  },
  parameters: {
    design: {
      type: "figma",
      url: "https://www.figma.com/file/4qNDv9mcu1ZWZkZxO3fVpP/6.0-Release?node-id=11331%3A239355",
    },
  },
}

const Template = (args, { argTypes }) => ({
  components: { HuxStartDate },
  props: Object.keys(argTypes),
  data() {
    return {}
  },
  template: `
    <div>
    <hux-start-date
    v-bind="$props"
    v-on="$props"
    />
        </div>`,
})

export const huxStartDate = Template.bind({})
