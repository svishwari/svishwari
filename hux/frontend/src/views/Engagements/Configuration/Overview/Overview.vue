<template>
  <div class="audience-insight-wrap">
    <div v-cloak>
      Audience
      <div class="row ma-0 mt-1">
        <metric-card
          v-for="(item, i) in Object.values(audienceOverview)"
          :key="i"
          class="mr-3"
          :grow="i === 0 ? 2 : 1"
          :title="item.title"
          :icon="item.icon"
          :height="80"
          :interactable="item.action ? true : false"
          :title-tooltip="item.titleTooltip"
          max-width="170"
          data-e2e="audience-overview"
        >
          <template #subtitle-extended>
            <tooltip>
              <template #label-content>
                <span class="font-weight-semi-bold">
                  {{ getFormattedValue(item) | Empty }}
                </span>
              </template>
              <template #hover-content>
                <span v-if="percentageColumns.includes(item.title)">
                  {{ item.subtitle | Percentage | Empty }}
                </span>
                <span v-else>{{ item.subtitle | Numeric | Empty }}</span>
              </template>
            </tooltip>
          </template>
        </metric-card>

        <metric-card
          class="mr-3"
          title="Gender"
          :height="80"
          max-width="220"
          :interactable="false"
        >
          <template #subtitle-extended>
            <tooltip>
              <template #label-content>
                <div class="men mr-1 font-weight-semi-bold">
                  M: {{ audienceInsights.gender_men | Percentage | Empty }}
                </div>
              </template>
              <template #hover-content>
                <span>
                  {{ audienceInsights.gender_men | Percentage | Empty }}
                </span>
              </template>
            </tooltip>

            <tooltip>
              <template #label-content>
                <div class="women mx-1 font-weight-semi-bold">
                  W: {{ audienceInsights.gender_women | Percentage | Empty }}
                </div>
              </template>
              <template #hover-content>
                <span>
                  {{ audienceInsights.gender_women | Percentage | Empty }}
                </span>
              </template>
            </tooltip>

            <tooltip>
              <template #label-content>
                <div class="other mx-1 font-weight-semi-bold">
                  O: {{ audienceInsights.gender_other | Percentage | Empty }}
                </div>
              </template>
              <template #hover-content>
                <span>
                  {{ audienceInsights.gender_other | Percentage | Empty }}
                </span>
              </template>
            </tooltip>
          </template>
        </metric-card>
      </div>
    </div>
  </div>
</template>

<script>
// helpers
import { mapGetters, mapActions } from "vuex"

// common components
import Icon from "@/components/common/Icon.vue"
import MetricCard from "@/components/common/MetricCard.vue"
import Tooltip from "@/components/common/Tooltip.vue"

export default {
  name: "Overview",
  components: {
    Icon,
    MetricCard,
    Tooltip,
  },
  props: {
    insights: {
      type: Object,
      required: false,
    },
  },
  data() {
    return {
      percentageColumns: ["Women", "Men", "Other"],
    }
  },
  computed: {
    ...mapGetters({}),

    audienceInsights() {
      return this.insights && this.insights.audience_insights
        ? this.insights.audience_insights
        : {}
    },
    audienceOverview() {
      const metrics = {
        total_customers: {
          title: "Size",
          subtitle: "",
          icon: "targetsize",
          titleTooltip:
            "Current number of customers who fit the selected attributes.",
          tooltipWidth: "231",
        },
        countries: { title: "Countries", subtitle: "", icon: "birth" },
        states: { title: "States", subtitle: "", icon: "birth" },
        cities: { title: "Cities", subtitle: "", icon: "birth" },
        age: { title: "Age range", subtitle: "", icon: "birth" },
      }
      const sizeValue  = this.insights && this.insights.size
      const insights = this.audienceInsights
      let result = Object.keys(metrics).map((metric) => {
        let metricCardSubtitle
        if (metric === "total_customers") {
          metricCardSubtitle = sizeValue
        }else if (metric === "countries") {
          metricCardSubtitle = insights.total_countries
        } else if (metric === "states") {
          metricCardSubtitle = insights.total_us_states
        } else if (metric === "cities") {
          metricCardSubtitle = insights.total_cities
        }
        return {
          ...metrics[metric],
          ...{
            subtitle:
              metric === "age"
                ? this.getAgeString(insights["min_age"], insights["max_age"])
                : metricCardSubtitle,
          },
        }
      })
      return result
    },
  },
  async mounted() {},

  updated() {},

  methods: {
    ...mapActions({}),
    getAgeString(min_age, max_age) {
      if (min_age && max_age && min_age === max_age) {
        return min_age
      } else if (min_age && max_age) {
        return `${min_age}-${max_age}`
      } else {
        return "-"
      }
    },
    /**
     * Formatting the values to the desired format using predefined application filters.
     *
     * @param {object} item item
     * @param {string} item.title item's title
     * @returns {number | string } formatted value
     */
    getFormattedValue(item) {
      switch (item.title) {
        case "Size":
          return this.$options.filters.Numeric(
            item.subtitle,
            false,
            false,
            true
          )
        case "Women":
        case "Men":
        case "Other":
          return this.$options.filters.Percentage(item.subtitle)
        default:
          return item.subtitle
      }
    },
  },
}
</script>
<style lang="scss" scoped></style>
