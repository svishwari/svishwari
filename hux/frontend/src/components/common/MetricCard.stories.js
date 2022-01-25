import MetricCard from "./MetricCard.vue"

export default {
  component: MetricCard,

  title: "Components",

  argTypes: {
    isModelRequested: { table: { disable: true } },
    isAdded: { table: { disable: true } },
    isAvailable: { table: { disable: true } },
    isAlreadyAdded: { table: { disable: true } },
    hideButton: { table: { disable: true } },
    enableBlueBackground: { table: { disable: true } },
    to: { table: { disable: true } },
    requestedButton: { table: { disable: true } },
    items: { table: { disable: true } },
    fields: { table: { disable: true } },
    empty: { table: { disable: true } },
    sort: { table: { disable: true } },
    bordered: { table: { disable: true } },
    selectedItems: { table: { disable: true } },
    toRight: { table: { disable: true } },
    value: { table: { disable: true } },
    width: { table: { disable: true } },
    expandedWidth: { table: { disable: true } },
    expandable: { table: { disable: true } },
    disableTransition: { table: { disable: true } },
    loading: { table: { disable: true } },
    contentPadding: { table: { disable: true } },
    contentHeaderPadding: { table: { disable: true } },
    headerHeight: { table: { disable: true } },
    step: { table: { disable: true } },
    label: { table: { disable: true } },
    optional: { table: { disable: true } },
    disabled: { table: { disable: true } },
    border: { table: { disable: true } },
    min: { table: { disable: true } },
    max: { table: { disable: true } },
    quired: { table: { disable: true } },
    isRangeSlider: { table: { disable: true } },
  },

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
