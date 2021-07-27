<template>
  <div class="audience-insight-wrap">
    <PageHeader class="background-border" :headerHeightChanges="'py-3'">
      <template #left>
        <Breadcrumb :items="items" />
      </template>
      <template #right>
        <v-icon size="22" color="lightGrey" class="mr-2"> mdi-refresh </v-icon>

        <v-icon size="22" color="lightGrey" class="icon-border pa-2 ma-1">
          mdi-plus-circle-multiple-outline
        </v-icon>
        <v-icon size="22" color="lightGrey" class="icon-border pa-2 ma-1">
          mdi-pencil
        </v-icon>
        <v-icon size="22" color="lightGrey" class="icon-border pa-2 ma-1">
          mdi-download
        </v-icon>
      </template>
    </PageHeader>
    <v-progress-linear :active="loading" :indeterminate="loading" />
    <div class="row px-15 my-1" v-if="audience && audience.audienceHistory">
      <MetricCard
        v-for="(item, i) in audience.audienceHistory"
        class="ma-4 audience-summary"
        :key="i"
        :grow="0"
        :title="item.title"
        :icon="item.icon"
      >
        <template #subtitle-extended>
          <span class="mr-2">
            <Tooltip>
              <template #label-content>
                <span class="neroBlack--text font-weight-semi-bold">
                  {{ getFormattedTime(item.subtitle) }}
                </span>
              </template>
              <template #hover-content>
                {{ item.subtitle | Date | Empty }}
              </template>
            </Tooltip>
          </span>
          <Avatar :name="item.fullName" />
        </template>
      </MetricCard>

      <MetricCard
        class="ma-4 audience-summary"
        :title="'Attributes'"
        v-if="Object.keys(appliedFilters).length > 0"
      >
        <template #extra-item>
          <div class="container pl-0">
            <ul class="filter-list">
              <li
                v-for="filterKey in Object.keys(appliedFilters)"
                :key="filterKey"
                class="filter-item ma-0 mr-1 d-flex align-center"
              >
                <icon
                  :type="filterKey == 'general' ? 'plus' : filterKey"
                  :size="filterKey == 'general' ? 10 : 21"
                  class="mr-1"
                />
                <!-- <span class="ml-1"></span> -->
                <tooltip
                  v-for="filter in Object.keys(appliedFilters[filterKey])"
                  :key="filter"
                >
                  <template #label-content>
                    <span
                      class="
                        neroBlack--text
                        font-weight-semi-bold
                        text-over-2
                        filter-title
                      "
                      v-html="appliedFilters[filterKey][filter].name"
                    />
                  </template>
                  <template #hover-content>
                    <span class="text-caption neroBlack--text">
                      <div class="mb-2">
                        {{ appliedFilters[filterKey][filter].name }}
                      </div>
                      <span v-html="appliedFilters[filterKey][filter].hover" />
                    </span>
                  </template>
                </tooltip>
              </li>
            </ul>
          </div>
        </template>
      </MetricCard>
    </div>
    <div class="px-15 my-1">
      <v-card class="rounded pa-5 box-shadow-5">
        <div class="overview">Audience overview</div>
        <div class="row overview-list mb-0 ml-0 mt-1">
          <MetricCard
            v-for="(item, i) in Object.keys(insightInfoItems)"
            class="mr-3"
            :key="i"
            :grow="i === 0 ? 2 : 1"
            :title="insightInfoItems[item].title"
            :icon="insightInfoItems[item].icon"
          >
            <template #subtitle-extended>
              <tooltip>
                <template #label-content>
                  <span class="font-weight-semi-bold">
                    {{ getFormattedValue(insightInfoItems[item]) }}
                  </span>
                </template>
                <template #hover-content>
                  {{ insightInfoItems[item].subtitle | Empty }}
                </template>
              </tooltip>
            </template>
          </MetricCard>
        </div>
      </v-card>
    </div>
    <v-row class="px-15 mt-2">
      <v-col cols="3">
        <income-chart></income-chart>
      </v-col>
    </v-row>

    <v-divider class="my-8"></v-divider>
    <EmptyStateChart>
      <template #chart-image>
        <img src="@/assets/images/empty-state-chart-3.png" alt="Empty state" />
      </template>
    </EmptyStateChart>
  </div>
</template>

<script>
import { generateColor } from "@/utils"
import { mapGetters, mapActions } from "vuex"
import PageHeader from "@/components/PageHeader"
import Breadcrumb from "@/components/common/Breadcrumb"
import Avatar from "@/components/common/Avatar"
import Tooltip from "../../components/common/Tooltip.vue"
import MetricCard from "@/components/common/MetricCard"
import EmptyStateChart from "@/components/common/EmptyStateChart"
import Icon from "../../components/common/Icon.vue"
import IncomeChart from "@/components/common/incomeChart/IncomeChart"

export default {
  name: "AudienceInsight",
  components: {
    MetricCard,
    EmptyStateChart,
    PageHeader,
    Breadcrumb,
    Avatar,
    Tooltip,
    Icon,
    IncomeChart,
  },
  data() {
    return {
      items: [
        {
          text: "Audiences",
          disabled: false,
          href: "/audiences",
          icon: "audiences",
        },
        {
          text: "",
          disabled: true,
          href: this.$route.path,
        },
      ],
      loading: false,
      insightInfoItems: {
        total_customers: {
          title: "Target size",
          subtitle: "",
        },
        total_countries: {
          title: "Countries",
          subtitle: "",
          icon: "mdi-earth",
        },
        total_us_states: { title: "US States", subtitle: "", icon: "mdi-map" },

        total_cities: {
          title: "Cities",
          subtitle: "",
          icon: "mdi-map-marker-radius",
        },
        max_age: { title: "Age", subtitle: "", icon: "mdi-cake-variant" },
        gender_women: {
          title: "Women",
          subtitle: "",
          icon: "mdi-gender-female",
        },
        gender_men: { title: "Men", subtitle: "", icon: "mdi-gender-male" },
        gender_other: {
          title: "Other",
          subtitle: "",
          icon: "mdi-gender-male-female",
        },
      },
      modelInitial: [
        { value: "propensity", icon: "model" },
        { value: "lifetime", icon: "lifetime" },
        { value: "churn", icon: "churn" },
      ],
    }
  },
  computed: {
    ...mapGetters({
      getAudience: "audiences/audience",
    }),
    audience() {
      return this.getAudience(this.$route.params.id)
    },

    /**
     * This computed property is converting the audience filters conditions
     * into groups of fiters and having custom keys which are needed
     * on the UI transformation.
     */
    appliedFilters() {
      try {
        let _filters = {}
        if (this.audience && this.audience.filters) {
          this.audience.filters.forEach((section) => {
            section.section_filters.forEach((filter) => {
              const model = this.modelInitial.filter(
                (model) =>
                  typeof filter.field === "string" &&
                  filter.field.includes(model.value)
              )
              const filterObj = {
                name: this.$options.filters.TitleCase(filter.field),
                key: filter.field,
              }

              filterObj.name = filterObj.name.replace(/_/gi, " ")
              if (model.length > 0) {
                filterObj["hover"] = "Between " + filter.value.join("-")
                if (!_filters[model[0].icon]) _filters[model[0].icon] = {}
                if (_filters[model[0].icon][filter.field])
                  _filters[model[0].icon][filter.field]["hover"] +=
                    "<br/> " + filterObj.hover
                else _filters[model[0].icon][filter.field] = filterObj
              } else {
                if (!_filters["general"]) _filters["general"] = {}
                filterObj["hover"] =
                  filter.type === "range"
                    ? "Include " + filter.value.join("-")
                    : filter.value
                if (_filters["general"][filter.field])
                  _filters["general"][filter.field]["hover"] +=
                    "<br/> " + filterObj.hover
                else _filters["general"][filter.field] = filterObj
              }
            })
          })
        }
        return _filters
      } catch (error) {
        return []
      }
    },
  },
  methods: {
    ...mapActions({
      getAudienceById: "audiences/getAudienceById",
    }),
    getFormattedTime(time) {
      return this.$options.filters.Date(time, "relative") + " by"
    },
    getColorCode(name) {
      return generateColor(name, 30, 60) + " !important"
    },

    /**
     * This is to map the Insight Values from the getter.
     */
    mapInsights() {
      this.insightInfoItems = Object.keys(this.insightInfoItems).map(
        (insight) => {
          return {
            title: this.insightInfoItems[insight].title,
            subtitle: this.audience.audience_insights[insight],
            icon: this.insightInfoItems[insight].icon,
          }
        }
      )
    },

    /**
     * Formatting the values to the desired format using predebfined application filters.
     */
    getFormattedValue(item) {
      switch (item.title) {
        case "Target size":
        case "Countries":
        case "US States":
        case "Cities":
          return this.$options.filters.Numeric(
            item.subtitle,
            false,
            false,
            true
          )
        case "Women":
        case "Men":
        case "Other":
          return this.$options.filters.percentageConvert(
            item.subtitle,
            true,
            true
          )
        default:
          return item.subtitle
      }
    },
  },
  async mounted() {
    this.loading = true
    await this.getAudienceById(this.$route.params.id)
    this.items[1].text = this.audience.name
    this.mapInsights()
    this.loading = false
  },
}
</script>
<style lang="scss" scoped>
.audience-insight-wrap {
  .container {
    ul {
      padding: 0;
      margin: 0;
      list-style-type: none;
    }
  }
  .audience-summary {
    padding: 10px 15px;
  }
  .container {
    .filter-list {
      .filter-item {
        width: fit-content;
        height: auto;
        float: left;
        margin-left: 2%;
        span {
          .filter-title {
            &::after {
              content: ",\00a0";
            }
          }
          &:last-child {
            .filter-title {
              &::after {
                content: "";
                margin-right: 8px;
              }
            }
          }
        }
      }
    }
  }
  .blue-grey {
    border-width: 2px;
    border-style: solid;
    border-radius: 50%;
    font-size: 14px;
    width: 35px;
    height: 35px;
    line-height: 22px;
    color: var(--v-neroBlack-base) !important;
    cursor: default !important;
    background: transparent !important;
  }
}
.icon-border {
  cursor: default;
}
</style>
