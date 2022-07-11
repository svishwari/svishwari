import MultiLineChart from "@/components/common/IDRMatchingTrend/MultiLineChart.vue"
import data from "./DensityChartData"

export default {
  component: MultiLineChart,

  title: "Charts/Multi Line Chart",

  args: {
    data: data,
    range: [100, 400],
    min: 0,
    max: 1000,
    id: "1",
    chartDimensions: {
      width: 1000,
      height: 100,
    },
  },

  parameters: {
    design: {
      type: "figma",
      url: "https://www.figma.com/file/4qNDv9mcu1ZWZkZxO3fVpP/6.0-Release?node-id=6852%3A140978",
    },
  },
}

const Template = (_, { argTypes }) => ({
  components: { MultiLineChart },
  props: Object.keys(argTypes),
  template: `
  <div>
    <div class="mb-5">
      For any param change to reflect on the chart change the id
    </div>
    <div>
      <multi-line-chart v-bind="$props" v-on="$props" />
    </div>
  </div>
  `,
})

export const DensityChart = Template.bind({})
