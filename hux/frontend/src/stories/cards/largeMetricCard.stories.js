import LargeMetricCard from "./LargeMetricCard.vue"
import CardStat from "@/components/common/Cards/Stat"
import AllIcons from "@/stories/icons/Icons"
export default {
  component: LargeMetricCard,
  title: "NewComponents/Cards",
  argTypes: {
    icon: {
      options: AllIcons,
      control: {
        type: "select",
      },
    },
    title: { control: { type: "text" } },
    description: { control: { type: "text" } },
    disabled: {
      control: { type: "boolean" },
    },
    actionMenu: {
      control: { type: "boolean" },
    },
    logoOption: {
      control: { type: "boolean" },
    },
    pill: { control: { type: "text" } },
  },
  args: {
    icon: "model",
    title: "Model Name",
    description: "Descriptive text for the model item chosen above",
    disabled: false,
    actionMenu: false,
    logoOption: false,
    iconColor: "Primary",
    actionMenu: true,
    status: "Active",
    pill: "Hungry",
  },
  parameters: {
    design: {
      type: "figma",
      url: "https://www.figma.com/file/4qNDv9mcu1ZWZkZxO3fVpP/6.0-Release?node-id=11331%3A228725",
    },
  },
}

const Template = (args, { argTypes }) => ({
  components: { LargeMetricCard, CardStat },
  props: Object.keys(argTypes),
  data() {
    return {
      model: {
        status: "Active",
        latest_version: "1.1.1",
        last_trained: "a date",
        fulcrum_date: "another date",
        lookback_window: "365",
        prediction_window: "60",
      },
    }
  },
  template: `
    <div>
    <large-metric-card
      v-bind="$props"
      v-on="$props"
    >
    <template slot="body">
      <v-row no-gutters>
        <v-col cols="5">
          <card-stat
            label="Version"
            :value="model.latest_version | Empty"
            stat-class="border-0"
          >
            <div class="mb-3">
              Trained date<br />
              {{ model.last_trained | Date | Empty }}
            </div>
            <div class="mb-3">
              Fulcrum date<br />
              {{ model.fulcrum_date | Date | Empty }}
            </div>
            <div class="mb-3">
              Lookback period (days)<br />
              {{ model.lookback_window }}
            </div>
            <div>
              Prediction period (days)<br />
              {{ model.prediction_window }}
            </div>
          </card-stat>
        </v-col>
        <v-col cols="7">
          <card-stat
            label="Last trained"
            :value="model.last_trained | Date('relative') | Empty"
            data-e2e="model-last-trained-date"
          >
            {{ model.last_trained | Date | Empty }}
          </card-stat>
        </v-col>
      </v-row>
    </template>
    <template slot="action-menu-options">
      <div
        class="px-4 py-2 white d-flex flex-column text-h5"
      >
        <span class="d-flex align-center"> Remove </span>
      </div>
    </template>
  </large-metric-card>
        </div>`,
})

export const largeMetricCard = Template.bind({})
