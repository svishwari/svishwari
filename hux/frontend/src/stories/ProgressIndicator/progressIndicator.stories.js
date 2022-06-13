import ProgressIndicator from "./ProgressIndicator.vue"

export default {
  component: ProgressIndicator,
  title: "NewComponents/ProgressIndicator",

  argTypes: {
    steps: { control: "array" },
    currrentStep: { control: "number" },
    errorSteps: { control: "array" },
  },

  args: {
    steps: ["Step1", "Step2", "Step3", "Step4", "Step5"],
    currentStep: 3,
    errorSteps: [2, 5],
  },

  parameters: {
    design: {
      type: "figma",
      url: "https://www.figma.com/file/eCWUinup52AoHQw1FBVJkd/HDS-(Hux-Design-System)?node-id=9432%3A67554",
    },
  },
}

const Template = (args, { argTypes }) => ({
  components: { ProgressIndicator },
  props: Object.keys(argTypes),
  template: '<progress-indicator v-bind="$props" />',
})

export const progressIndicator = Template.bind({})
