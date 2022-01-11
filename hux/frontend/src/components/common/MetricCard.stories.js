import MetricCard from "./MetricCard.vue"

export default {
  component: MetricCard,

  title: "Components",

  parameters: {
    design: {
      type: "figma",
      url: "https://www.figma.com/file/4qNDv9mcu1ZWZkZxO3fVpP/6.0-Release?node-id=6852%3A108904",
    },
  },
}

const Template = () => ({
  components: { MetricCard },
  template: `<metric-card
    class="ma-4"
    title="Metric Title"
    :max-width="203"
    :height="75"
    :interactable="false"
  >
    <template #subtitle-extended>
      <div class="text-subtitle-1 black--text text--darken-4 mb-2">
        <icon class="mr-1" type="stock-up" :size="8" color="success" />
        <icon class="ml-1 mr-1" type="stock-down" :size="8" color="error" />
        01/01/21 • 9:42AM
      </div>
    </template>
  </metric-card>`,
})

export const metricCard = Template.bind({})
