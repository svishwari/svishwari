<template>
  <v-card class="overview-card rounded-lg card-shadow py-4 px-6" height="323">
    <v-card-title class="d-flex justify-space-between pa-0">
      <h3 class="text-h3">Overview</h3>
      <div class="d-flex align-center">
        <icon
          type="timestamp"
          color="black"
          variant="lighten4"
          :size="14"
          class="mr-1"
        />
        <span class="text-body-2 black--text text--lighten-4">
          Today {{ lastRefreshed | Date("hh:mm A", (local = true)) }}
        </span>
      </div>
    </v-card-title>
    <v-card-text
      class="pa-0 mt-3 d-flex flex-wrap flex-row space-between card-wrap"
    >
      <metric-card
        v-for="card in infoCards"
        :key="card.id"
        :title="card.title"
        :title-tooltip="card.helpText"
        :tooltip-width="card.helpWidth"
      >
        <template #subtitle-extended>
          <v-progress-linear
            v-if="loading"
            class="mt-2 mr-6"
            indeterminate
            buffer-value="0"
            stream
            rouded
          />
          <tooltip v-else-if="card.format !== 'multiple'">
            <template #label-content>
              <span class="black--text text-subtitle-1 mt-1 pb-0 d-block">
                <span v-if="card.format == 'relative'">
                  {{ getValue(card.title) | Numeric(true, false, true) }}
                </span>
                <span v-else>
                  {{ getValue(card.title) }}
                </span>
              </span>
            </template>
            <template #hover-content>
              <span v-if="card.format != 'multiple'">
                {{ getValue(card.title) }}
              </span>
            </template>
          </tooltip>
          <span
            v-else-if="card.format == 'multiple'"
            class="black--text text-subtitle-1 mt-1 pb-0 d-block"
          >
            <span
              v-for="gender in getValue(card.title)"
              :key="gender.id"
              class="mr-2"
              :class="{
                'black--text text--lighten-3': gender.value === 0,
              }"
            >
              {{ gender.key }}:
              <tooltip>
                <template #label-content>
                  {{ gender.value | Percentage() }}
                </template>
                <template #hover-content>
                  {{ gender.value }}
                </template>
              </tooltip>
            </span>
          </span>
        </template>
      </metric-card>
    </v-card-text>
  </v-card>
</template>

<script>
import Icon from "../../components/common/Icon.vue"
import MetricCard from "../../components/common/MetricCard.vue"
import Tooltip from "../../components/common/Tooltip.vue"

export default {
  name: "Ovefrview",
  components: { Icon, MetricCard, Tooltip },
  props: {
    data: {
      type: Object,
      required: false,
      default: () => {},
    },
    loading: {
      type: Boolean,
      required: false,
      default: false,
    },
    lastRefreshed: {
      type: Date,
      required: false,
    },
  },
  data() {
    return {
      infoCards: [
        {
          title: "Size",
          format: "relative",
          helpText:
            "Current number of customers who fit the selected attributes.",
          helpWidth: 232,
        },
        {
          title: "Age Range",
          value: "24-68",
        },
        {
          title: "Countries",
          value: "1",
        },
        {
          title: "States",
          value: "50",
          helpText:
            "US states or regions equivalent to US state-level (e.g. counties, districts, departments, divisions, parishes, provinces, etc).",
          helpWidth: 283,
        },
        {
          title: "Gender",
          format: "multiple",
          value: "Women",
        },
      ],
    }
  },
  methods: {
    getValue(type) {
      switch (type) {
        case "Size":
          return this.data.total_customers
        case "Age Range":
          return `${this.data.min_age}-${this.data.max_age}`
        case "Countries":
          return this.data.total_countries
        case "States":
          return this.data.total_us_states
        default:
          // Gender
          return [
            {
              key: "M",
              value: this.data.gender_men,
            },
            {
              key: "W",
              value: this.data.gender_women,
            },
            {
              key: "O",
              value: this.data.gender_other,
            },
          ]
      }
    },
  },
}
</script>

<style lang="scss" scoped>
.overview-card {
  background: var(--v-primary-lighten1);
  .card-wrap {
    gap: 12px;
    flex: 0 0 50%;
  }
  .metric-card-wrapper {
    background: var(--v-white-base);
    flex-basis: calc(50% - (12px * 2));
    &:last-child {
      flex-grow: inherit !important;
      min-width: 220px;
    }
    ::v-deep .pb-1 {
      padding-bottom: 0px !important;
    }
  }
}
</style>
