import DescriptiveCard from "./DescriptiveCard.vue"
import CardStat from "@/components/common/Cards/Stat"
import Status from "@/components/common/Status"
import AllIcons from "@/stories/icons/Icons"
export default {
  component: DescriptiveCard,
  title: "Components/Cards",
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
    comingSoon: { control: { type: "boolean" } },
    height: {
      control: { type: "text" },
    },
    width: {
      control: { type: "text" },
    },
    dotOption: {
      control: { type: "text" },
    },
    logoOption: {
      control: { type: "boolean" },
    },
    interactable: {
      control: { type: "boolean" },
      iconColor: {
        control: { type: "text" },
      },
    },
  },
  args: {
    icon: "model",
    title: "Model Name",
    description: "Descriptive text for the model item chosen above",
    disabled: false,
    actionMenu: false,
    comingSoon: false,
    height: "255",
    width: "280",
    dotOption: "Activate",
    logoOption: false,
    interactable: false,
    iconColor: "Primary",
  },
  parameters: {
    design: {
      type: "figma",
      url: "https://www.figma.com/file/4qNDv9mcu1ZWZkZxO3fVpP/6.0-Release?node-id=11331%3A228725",
    },
  },
}

const Template = (args, { argTypes }) => ({
  components: { DescriptiveCard, CardStat, Status },
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
    <descriptive-card
    v-bind="$props"
    v-on="$props"
  >
    <template slot="top">
      <status
        :icon-size="18"
        :status="model.status"
        collapsed
        class="d-flex float-left"
      />
    </template>

    <template slot="default">
      <v-row no-gutters class="mt-4">
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
  </descriptive-card>
        </div>`,
})

export const descriptiveCard = Template.bind({})
