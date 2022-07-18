import HuxDataTable from "./HuxDataTable"
import Status from "../status/Status2.vue"
import Size from "@/components/common/huxTable/Size.vue"

export default {
  component: HuxDataTable,

  title: "NewComponents",

  argTypes: {
    dataItems: { control: { type: "array" } },
    columns: { control: { type: "array" } },
  },

  args: {
    dataItems: [
      {
        profile_size_percent: 1.06,
        bucket: 10,
        predicted_lift: 9.73,
        profile_count: 22,
        actual_rate: 822.86,
        actual_lift: 11.37,
        predicted_value: 10000.69,
        actual_value: 9728.81,
        predicted_rate: 714.65,
      },
      {
        profile_size_percent: 1.02,
        bucket: 20,
        predicted_lift: 7.21,
        profile_count: 54,
        actual_rate: 588.54,
        actual_lift: 8.31,
        predicted_value: 18000.69,
        actual_value: 17280.81,
        predicted_rate: 529.41,
      },
      {
        profile_size_percent: 2.61,
        bucket: 30,
        predicted_lift: 5.75,
        profile_count: 102,
        actual_rate: 455.82,
        actual_lift: 6.3,
        predicted_value: 45000.69,
        actual_value: 47280.81,
        predicted_rate: 422,
      },
      {
        profile_size_percent: 4.96,
        bucket: 40,
        predicted_lift: 4.43,
        profile_count: 190,
        actual_rate: 323.12,
        actual_lift: 4.47,
        predicted_value: 70000.69,
        actual_value: 67280.81,
        predicted_rate: 325.44,
      },
      {
        profile_size_percent: 9.19,
        bucket: 50,
        predicted_lift: 3.58,
        profile_count: 300,
        actual_rate: 253.44,
        actual_lift: 3.5,
        predicted_value: 80000.69,
        actual_value: 77280.81,
        predicted_rate: 262.98,
      },
      {
        profile_size_percent: 14.51,
        bucket: 60,
        predicted_lift: 2.99,
        profile_count: 427,
        actual_rate: 212.49,
        actual_lift: 2.94,
        predicted_value: 97123.69,
        actual_value: 87280.81,
        predicted_rate: 219.54,
      },
      {
        profile_size_percent: 20.66,
        bucket: 70,
        predicted_lift: 2.45,
        profile_count: 612,
        actual_rate: 171.91,
        actual_lift: 2.38,
        predicted_value: 123456.69,
        actual_value: 97280.81,
        predicted_rate: 179.57,
      },
      {
        profile_size_percent: 29.61,
        bucket: 80,
        predicted_lift: 2.04,
        profile_count: 818,
        actual_rate: 146.93,
        actual_lift: 2.03,
        predicted_value: 152342.69,
        actual_value: 142800.81,
        predicted_rate: 149.98,
      },
      {
        profile_size_percent: 39.57,
        bucket: 90,
        predicted_lift: 1.53,
        profile_count: 1226,
        actual_rate: 109.94,
        actual_lift: 1.52,
        predicted_value: 167000.69,
        actual_value: 152800.81,
        predicted_rate: 112.51,
      },
      {
        profile_size_percent: 100,
        bucket: 100,
        predicted_lift: 1,
        profile_count: 2067,
        actual_rate: 72.36,
        actual_lift: 1,
        predicted_value: 200000.69,
        actual_value: 172800.81,
        predicted_rate: 73.43,
      },
    ],

    columns: [
      { text: "Bucket", value: "bucket", width: "94px" },
      { text: "Predicted ", value: "predicted_value", width: "117px" },
      { text: "Actual ", value: "actual_value", width: "117px" },
      { text: "Profiles", value: "profile_count", width: "117px" },
      {
        text: "Rate <span class='pt-2'>(predicted)</span>",
        value: "predicted_rate",
        width: "117px",
      },
      {
        text: "Rate <span class='pt-2'>(actual)</span>",
        value: "actual_rate",
        width: "117px",
      },
      {
        text: "Lift <span class='pt-2'>(predicted)</span>",
        value: "predicted_lift",
        width: "117px",
      },
      {
        text: "Lift <span class='pt-2'>(actual)</span>",
        value: "actual_lift",
        width: "117px",
      },
      {
        text: "Size % <span class='pt-2'>(profiles)</span>",
        value: "profile_size_percent",
        width: "117px",
      },
    ],
  },

  parameters: {
    design: {
      type: "figma",
      url: "https://www.figma.com/file/4qNDv9mcu1ZWZkZxO3fVpP/6.0-Release?node-id=11331%3A223042",
    },
  },
}

const Template = (args, { argTypes }) => ({
  components: { HuxDataTable, Status, Size },
  props: Object.keys(argTypes),
  computed: {
    headers() {
      return args.columns
    },
  },
  template: `
  <hux-data-table v-bind="$props" v-on="$props">
  <template #row-item="{ item }">
    <td
      v-for="header in headers"
      :key="header.value"
    >
      <div>
        {{ item[header.value].toLocaleString() }}
      </div>
    </td>
  </template>
</hux-data-table>
`,
})

export const huxDataTable = Template.bind({})
