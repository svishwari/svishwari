<template>
  <div class="audience-insight-wrap">
    <PageHeader class="background-border">
      <template slot="left">
        <Breadcrumb :items="items" />
      </template>
      <template slot="right">
        <v-icon large :disabled="true"> mdi-refresh </v-icon>
        <v-icon size="22" class="icon-border pa-2 ma-1">
          mdi-plus-circle-multiple-outline
        </v-icon>
        <v-icon size="22" class="icon-border pa-2 ma-1"> mdi-pencil </v-icon>
        <v-icon size="22" class="icon-border pa-2 ma-1"> mdi-download </v-icon>
      </template>
    </PageHeader>
    <v-progress-linear :active="loading" :indeterminate="loading" />
    <div class="row px-15 my-1" v-if="audience && audience.audienceHistory">
      <MetricCard
        v-for="(item, i) in audience.audienceHistory"
        class="ma-4"
        :key="i"
        :grow="0"
        :title="item.title"
        :icon="item.icon"
      >
        <template #subtitle-extended>
          <span class="mr-2">
            <Tooltip>
              <template #label-content>
                {{ getFormattedTime(item.subtitle) }}
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
        class="ma-4"
        :title="'Attributes'"
        v-if="appliedFilters.length > 0"
      >
        <template slot="extra-item">
          <div class="container pl-0">
            <ul>
              <li v-for="filter in appliedFilters" :key="filter.id">
                <churn v-if="filter.icon == 'churn'" />
                <lifetimeValue v-if="filter.icon == 'lifetime'" />
                <plus v-if="filter.icon == 'plus'" />
                {{ filter.name | TitleCase }}
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
            v-for="(item, i) in insightInfoItems"
            class="mr-3"
            :key="i"
            :grow="i === 0 ? 2 : 1"
            :title="item.title"
            :icon="item.icon"
          >
            <template #subtitle-extended>
              <tooltip>
                <template #label-content>
                  <span class="font-weight-semi-bold">
                    {{ getFormattedValue(item) }}
                  </span>
                </template>
                <template #hover-content>
                  {{ item.subtitle | Empty }}
                </template>
              </tooltip>
            </template>
          </MetricCard>
        </div>
      </v-card>
    </div>
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
import lifetimeValue from "@/assets/images/lifetimeValue.svg"
import churn from "@/assets/images/churn.svg"
import plus from "@/assets/images/plus.svg"
export default {
  name: "AudienceInsight",
  components: {
    MetricCard,
    EmptyStateChart,
    PageHeader,
    Breadcrumb,
    Avatar,
    Tooltip,
    lifetimeValue,
    churn,
    plus,
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
      insightInfoItems: [
        { title: "Target size", subtitle: "" },
        { title: "Countries", subtitle: "", icon: "mdi-earth" },
        { title: "US States", subtitle: "", icon: "mdi-map" },
        { title: "Cities", subtitle: "", icon: "mdi-map-marker-radius" },
        { title: "Age", subtitle: "", icon: "mdi-cake-variant" },
        { title: "Women", subtitle: "", icon: "mdi-gender-female" },
        { title: "Men", subtitle: "", icon: "mdi-gender-male" },
        { title: "Other", subtitle: "", icon: "mdi-gender-male-female" },
      ],
      modelInitial: [{ value: "propensity", icon: "churn" }],
    }
  },
  computed: {
    ...mapGetters({
      getAudience: "audiences/audience",
    }),
    audience() {
      return this.getAudience(this.$route.params.id)
    },
    appliedFilters() {
      let _filters = []
      if (this.audience && this.audience.filters) {
        this.audience.filters.forEach((section) => {
          section.section_filters.forEach((filter) => {
            if (
              _filters.findIndex((item) =>
                item.name.toLowerCase().includes(filter.field)
              ) !== -1
            )
              return

            const filterObj = {
              name: this.$options.filters.TitleCase(filter.field),
            }
            const model = this.modelInitial.filter((model) =>
              filter.field.includes(model.value)
            )
            if (model.length > 0) {
              filterObj["icon"] = model[0].icon
              filterObj["sortOrder"] = 0
              _filters.push(filterObj)
            } else {
              const _plusFilter = _filters.filter(
                (item) => item.icon === "plus"
              )
              if (_plusFilter.length > 0) {
                _plusFilter[0].name +=
                  "," + this.$options.filters.TitleCase(filter.field)
                _plusFilter[0].name = _plusFilter[0].name
                  .split(",")
                  .sort()
                  .join(", ")
              } else {
                filterObj["icon"] = "plus"
                filterObj["sortOrder"] = 1
                _filters.push(filterObj)
              }
            }
          })
        })
      }
      return _filters.sort((a, b) => (a.sortOrder > b.sortOrder ? 1 : -1))
    },
  },
  methods: {
    ...mapActions({
      getAudienceById: "audiences/getAudienceById",
    }),
    refresh() {},
    getFormattedTime(time) {
      return this.$options.filters.Date(time, "relative") + " by"
    },
    getColorCode(name) {
      return generateColor(name, 30, 60) + " !important"
    },

    /**
     *
     */
    mapInsights() {
      this.insightInfoItems[0].subtitle =
        this.audience.audience_insights.total_customers
      this.insightInfoItems[1].subtitle =
        this.audience.audience_insights.total_countries
      this.insightInfoItems[2].subtitle =
        this.audience.audience_insights.total_us_states
      this.insightInfoItems[3].subtitle =
        this.audience.audience_insights.total_cities
      this.insightInfoItems[4].subtitle =
        this.audience.audience_insights.max_age
      this.insightInfoItems[5].subtitle =
        this.audience.audience_insights.gender_women
      this.insightInfoItems[6].subtitle =
        this.audience.audience_insights.gender_men
      this.insightInfoItems[7].subtitle =
        this.audience.audience_insights.gender_other
    },

    /**
     *
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
  .container {
    ul {
      li {
        width: fit-content;
        height: auto;
        float: left;
        margin-left: 2%;
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
</style>
