<template>
  <div class="summary-wrap d-flex mb-6">
    <metric-card
      class="mr-3 pt-4 shrink"
      :title="summaryCards[0].title"
      :height="75"
    >
      <template #subtitle-extended>
        <tooltip :max-width="280">
          <template #label-content>
            <span class="text-subtitle-1 black--text">{{
              data.delivery_schedule | DeliverySchedule
            }}</span>
          </template>
          <template #hover-content>
            <span v-if="!data.delivery_schedule">
              This engagement was delivered manually on
              {{ lastDelivered | Date("MMM D, YYYY [at] h:mm A") | Empty }}
            </span>
            <hux-delivery-text
              v-else
              :schedule="
                data.delivery_schedule ? data.delivery_schedule.schedule : {}
              "
              :start-date="
                data.delivery_schedule ? data.delivery_schedule.start_date : ''
              "
              :end-date="
                data.delivery_schedule ? data.delivery_schedule.end_date : ''
              "
            />
          </template>
        </tooltip>
      </template>
    </metric-card>
    <metric-card
      class="mr-3 pt-4 shrink"
      :title="summaryCards[1].title"
      :height="75"
    >
      <template #subtitle-extended>
        <span class="mr-2">
          <tooltip>
            <template #label-content>
              <span
                data-e2e="updated-metric"
                class="text-subtitle-1 black--text"
              >
                {{ summaryCards[1].value }}
              </span>
            </template>
            <template #hover-content>
              {{ summaryCards[1].hoverValue }}
            </template>
          </tooltip>
        </span>
      </template>
    </metric-card>
    <metric-card
      class="mr-3 pt-4 grow"
      :title="summaryCards[2].title"
      max-width="100%"
      :height="75"
    >
      <template #subtitle-extended>
        <span class="mr-2">
          <tooltip>
            <template #label-content>
              <span
                data-e2e="updated-metric"
                class="text-body-1 black--text text--darken-4"
              >
                {{ summaryCards[2].value }}
              </span>
            </template>
            <template #hover-content>
              {{ summaryCards[2].value }}
            </template>
          </tooltip>
        </span>
      </template>
    </metric-card>
  </div>
</template>

<script>
import MetricCard from "@/components/common/MetricCard"
import Tooltip from "@/components/common/Tooltip.vue"
import HuxDeliveryText from "@/components/common/DatePicker/HuxDeliveryText.vue"

export default {
  name: "EngagementOverviewSummary",
  components: {
    MetricCard,
    Tooltip,
    HuxDeliveryText,
  },
  props: {
    data: {
      type: Object,
      required: true,
      default: () => {},
    },
  },
  computed: {
    summaryCards() {
      const summary = [
        {
          id: 1,
          title: "Delivery schedule",
          value: this.fetchKey(this.data, "delivery_schedule"),
          subLabel: null,
        },
        {
          id: 2,
          title: "Target Size",
          value: this.fetchKey(this.data, "size"),
          subLabel: null,
        },
        {
          id: 3,
          title: "Description",
          value: this.fetchKey(this.data, "description"),
          subLabel: null,
        },
      ]
      return summary.filter((item) => item.title !== null)
    },
    deliverySchedule() {
      if (this.data && this.data.delivery_schedule) {
        if (
          !this.data.delivery_schedule.start_date &&
          !this.data.delivery_schedule.end_date
        ) {
          return "Now"
        } else {
          if (
            this.data.delivery_schedule.start_date &&
            this.data.delivery_schedule.end_date
          ) {
            return (
              this.$options.filters.Date(
                this.data.delivery_schedule.start_date,
                "MMMM D"
              ) +
              " - " +
              this.$options.filters.Date(
                this.data.delivery_schedule.end_date,
                "MMMM D"
              )
            )
          } else if (this.data.delivery_schedule.start_date) {
            return this.$options.filters.Date(
              this.data.delivery_schedule.start_date,
              "MMMM D"
            )
          } else if (this.data.delivery_schedule.end_date) {
            return this.$options.filters.Date(
              this.data.delivery_schedule.end_date,
              "MMMM D"
            )
          }
        }
      }
      return "Manual"
    },
    lastDelivered() {
      if (this.data.delivery_schedule !== null) {
        return ""
      } else {
        let audiences = JSON.parse(JSON.stringify(this.data.audiences))
        let last_delivered = ""
        audiences.map((audience) => {
          audience.destinations.map((destination) => {
            if (destination.latest_delivery?.update_time) {
              if (destination.latest_delivery.update_time > last_delivered) {
                last_delivered = destination.latest_delivery.update_time
              }
            }
          })
        })
        return last_delivered ? last_delivered : "-"
      }
    },
  },
  methods: {
    formattedDate(value) {
      if (value) {
        return this.$options.filters.Date(value, "relative") + " by"
      }
      return "-"
    },
    fetchKey(obj, key) {
      return obj && obj[key] ? obj[key] : "-"
    },
  },
}
</script>

<style lang="scss" scoped>
.summary-wrap {
  ::v-deep .metric-card-wrapper {
    .subtitle-slot {
      .avatar {
        margin-top: -6px !important;
      }
    }
  }
}
</style>
