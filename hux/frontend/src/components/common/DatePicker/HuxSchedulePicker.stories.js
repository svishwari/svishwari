import HuxSchedulePicker from "./HuxSchedulePicker.vue"

export default {
  component: HuxSchedulePicker,
  title: "Components/DatePicker",
  argTypes: {
    value: {
      control: { type: "object" },
    },
    startDate: {
      control: { type: "text" },
    },
    endDate: {
      control: { type: "text" },
    },
  },
  args: {
    value: [],
    startDate: "",
    endDate: "",
  },
  parameters: {},
}

const Template = (args, { argTypes }) => ({
  components: { HuxSchedulePicker },
  props: Object.keys(argTypes),
  data() {
    return {}
  },
  template: `
    <div>
    <hux-schedule-picker
        v-bind="$props"
        v-on="$props"
      />
        </div>`,
})

export const huxSchedulePicker = Template.bind({})
