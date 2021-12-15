import CardStat from "@/components/common/Cards/Stat"
export default {
  component: CardStat,
  title: "Components/Cards",
  argTypes: {
    label: {
      control: { type: "text" },
    },
    value: {
      control: { type: "text" },
    },
    statClass: {
      control: { type: "text" },
    },
  },
  args: {
    label: "Version",
    value: "1.1.1",
    statClass: "border-3",
  },
  parameters: {},
}

const Template = (args, { argTypes }) => ({
  components: { CardStat },
  props: Object.keys(argTypes),
  data() {
    return {
      model: {
        last_trained: "a date",
        fulcrum_date: "another date",
        lookback_window: "365",
        prediction_window: "60",
      },
    }
  },
  template: `
    <div>
    <card-stat
    v-bind="$props"
    v-on="$props"
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
        </div>`,
})

export const cardStat = Template.bind({})
