import MultiLineChart from "@/components/common/IDRMatchingTrend/MultiLineChart.vue"
import data from "./MultiLineChartData.js"

export default {
  component: MultiLineChart,

  title: "Charts/Multi Line Chart",

  args: {
    value: data,
    colorCodes: ["#005587", "#42EFFD", "#0C9DDB"],
    chartDimensions: { width: 1606, height: 300 },
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
      Multi Line Chart
    </div>
    <div>
      <multi-line-chart v-bind="$props" v-on="$props" />
    </div>
  </div>
  `,
})

export const AMultiLineChart = Template.bind({})
