import TimePicker from "./TimePicker.vue"
import AllIcons from "../icons/Icons"

export default {
  component: TimePicker,
  title: "NewComponents/TimePicker",
  argTypes: {
    hour: {
      options: [
        "01",
        "02",
        "03",
        "04",
        "05",
        "06",
        "07",
        "08",
        "09",
        "10",
        "11",
        "12",
      ],
      control: "select",
    },
    minute: {
      options: [
        "00",
        "05",
        "10",
        "15",
        "20",
        "25",
        "30",
        "35",
        "40",
        "45",
        "50",
        "55",
      ],
      control: "select",
    },
    zone: {
      options: ["AM", "PM"],
      control: "select",
    },
    icon: {
      options: AllIcons,
      control: "select",
    },
    showCheckMark: {
      control: { type: "boolean" },
    },
  },
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
