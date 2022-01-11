import HuxEndDate from "./HuxEndDate.vue"

export default {
  component: HuxEndDate,
  title: "Components/DatePicker",
  argTypes: {
    selected: {
      control: { type: "text" },
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
    isSubMenu: {
      control: { type: "boolean" },
    },
    transition: {
      options: ["scale-transition", "slide-x-transition", "slide-y-transition"],
      control: { type: "select" },
    },
    maxDate: {
      control: { type: "text" },
    },
    minDate: {
      control: { type: "text" },
    },
    isDisabled: {
      control: { type: "boolean" },
    },
  },
  args: {
    selected: "Select date",
    label: "Select Option",
    isOffsetX: false,
    isOffsetY: true,
    isOpenOnHover: false,
    isSubMenu: false,
    transition: "scale-transition",
    maxDate: "",
    minDate: "",
    isDisabled: false,
  },
  parameters: {
    design: {
      type: "figma",
      url: "https://www.figma.com/file/4qNDv9mcu1ZWZkZxO3fVpP/6.0-Release?node-id=11331%3A239355",
    },
  },
}

const Template = (args, { argTypes }) => ({
  components: { HuxEndDate },
  props: Object.keys(argTypes),
  data() {
    return {}
  },
  template: `
    <div style="width:30%">
    <hux-end-date
    v-bind="$props"
    v-on="$props"
    />
        </div>`,
})

export const huxEndDate = Template.bind({})
