import HuxSlider from "./HuxSlider.vue"

export default {
  component: HuxSlider,
  title: "Components",
  args: {
    value: [0.25, 0.65],
    min: 0,
    max: 1,
    quired: false,
    step: 0.05,
    isRangeSlider: true,
  },
  parameters: {},
}

const Template = (args, { argTypes }) => ({
  components: { HuxSlider },
  props: Object.keys(argTypes),
  data() {
    return {}
  },
  template: `
    <div class="pa-6" style="width:40%">
    <hux-slider
        v-bind="$props"
        v-on="$props"
      />
        </div>`,
})

export const huxSlider = Template.bind({})
