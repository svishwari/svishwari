<template>
  <div class="summary-wrap d-flex mb-6">
    <metric-card
      class="mr-3 pt-4 shrink"
      :title="summaryCards[0].title"
      :height="75"
    >
      <template #subtitle-extended>
        <div class="mb-2" data-e2e="delivery-schedule-metric">
          {{ deliverySchedule }}
        </div>
      </template>
    </metric-card>
    <metric-card
      class="mr-3 pt-4 shrink"
      :title="summaryCards[1].title"
      :height="75"
    >
      <template v-if="summaryCards[1].subLabel" #subtitle-extended>
        <span class="mr-2">
          <tooltip>
            <template #label-content>
              <span
                data-e2e="updated-metric"
                class="black--text text--darken-4"
              >
                {{ summaryCards[1].value }}
              </span>
            </template>
            <template #hover-content>
              {{ summaryCards[1].hoverValue | Date | Empty }}
            </template>
          </tooltip>
        </span>
        <span class="avatar">
          <avatar :name="summaryCards[1].subLabel" />
        </span>
      </template>
    </metric-card>
    <metric-card
      class="mr-3 pt-4 shrink"
      :title="summaryCards[2].title"
      :height="75"
    >
      <template v-if="summaryCards[2].subLabel" #subtitle-extended>
        <span class="mr-2">
          <tooltip>
            <template #label-content>
              <span
                class="black--text text--darken-4"
                data-e2e="created-metric"
              >
                {{ summaryCards[2].value }}
              </span>
            </template>
            <template #hover-content>
              {{ summaryCards[2].hoverValue | Date | Empty }}
            </template>
          </tooltip>
        </span>
        <span class="avatar">
          <avatar :name="summaryCards[2].subLabel" />
        </span>
      </template>
    </metric-card>
    <metric-card
      v-if="data && data.description"
      class="grow"
      title=""
      max-width="100%"
      :height="75"
    >
      <template #subtitle-extended>
        <span class="text--subtitle-1">
          {{ summaryCards[3].title }}
        </span>
      </template>
    </metric-card>
  </div>
</template>

<script>
import MetricCard from "@/components/common/MetricCard"
import Avatar from "@/components/common/Avatar"
import Tooltip from "../../components/common/Tooltip.vue"

export default {
  name: "EngagementOverviewSummary",
  components: {
    MetricCard,
    Avatar,
    Tooltip,
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
          title: "Last updated",
          // TODO: need to remove mapping to created by
          value:
            this.formattedDate(this.fetchKey(this.data, "update_time")) !== "-"
              ? this.formattedDate(this.fetchKey(this.data, "update_time"))
              : this.formattedDate(this.fetchKey(this.data, "create_time")),
          hoverValue:
            this.fetchKey(this.data, "update_time") !== "-"
              ? this.fetchKey(this.data, "update_time")
              : this.fetchKey(this.data, "create_time"),
          subLabel:
            this.fetchKey(this.data, "updated_by") !== "-"
              ? this.fetchKey(this.data, "updated_by")
              : this.fetchKey(this.data, "created_by"),
          width: "19%",
          minWidth: "164px",
        },
        {
          id: 3,
          title: "Created",
          value: this.formattedDate(this.fetchKey(this.data, "create_time")),
          hoverValue: this.fetchKey(this.data, "create_time"),
          subLabel: this.fetchKey(this.data, "created_by"),
          width: "19%",
          minWidth: "164px",
        },
        {
          id: 4,
          title: this.fetchKey(this.data, "description"),
          value: null,
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
