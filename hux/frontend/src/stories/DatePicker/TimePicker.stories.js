import TimePicker from "./TimePicker.vue"

export default {
  component: TimePicker,
  title: "NewComponents/DatePicker",
  argTypes: {},
  args: {},
  parameters: {
    design: {
      type: "figma",
      url: "https://www.figma.com/file/4qNDv9mcu1ZWZkZxO3fVpP/6.0-Release?node-id=11331%3A239355",
    },
  },
}

const Template = (args, { argTypes }) => ({
  components: { TimePicker },
  props: Object.keys(argTypes),
  data() {
    return {}
  },
  template: `
    <div>
      <time-picker
      v-bind="$props"
      v-on="$props"
    />
    </div>`,
})

export const timePicker = Template.bind({})
