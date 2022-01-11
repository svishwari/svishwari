<template>
  <drawer
    v-model="localToggle"
    class="add-audience-drawer-wrapper"
    :width="drawerWidth"
    :loading="loading"
    @onClose="closeDrawer()"
  >
    <template #header-left>
      <h3 class="text-h2">Create a new audience</h3>
    </template>

    <template #default>
      <div class="pa-6">
        <h6 class="pt-2 pb-6 text-body-1">
          Build a target audience from the data you own.
        </h6>
        <v-form ref="newAudienceRef" v-model="newAudienceValidity">
          <text-field
            v-model="newAudience.name"
            label-text="Audience name"
            placeholder="Name"
            class="audience-name-field"
            :rules="newAudienceRules"
            required
          />
        </v-form>
        <div class="pb-2 black--text text--darken-4 text-caption">
          Audience overview
        </div>
        <div class="d-flex align-center pb-4">
          <metric-card
            v-for="card in infoCards"
            :key="card.id"
            :title="card.title"
            :icon="card.icon"
            :title-tooltip="card.helpText"
            :tooltip-width="card.helpWidth"
            class="mr-2"
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
        </div>
        <hr class="black lighten-2 mb-4" />
        <div class="pt-1 pr-0">
          <attribute-rules
            :rules="attributeRules"
            apply-caption-style
            enable-title
          />
        </div>
      </div>
    </template>

    <template #footer-left>
      <hux-button
        size="large"
        is-tile
        variant="white"
        class="btn-border box-shadow-none"
        @click="onCancelAndBack()"
      >
        <span class="primary--text">Cancel &amp; back</span>
      </hux-button>
      <hux-button
        :disabled="!newAudienceValidity"
        is-tile
        color="primary"
        @click="add()"
      >
        Create &amp; add
      </hux-button>
    </template>
  </drawer>
</template>

<script>
import { mapGetters, mapActions } from "vuex"
import Drawer from "@/components/common/Drawer.vue"
import TextField from "@/components/common/TextField"
import MetricCard from "@/components/common/MetricCard"
import AttributeRules from "@/views/SegmentPlayground/AttributeRules.vue"
import Tooltip from "@/components/common/Tooltip"
import huxButton from "@/components/common/huxButton"

export default {
  name: "AddAudienceDrawer",

  components: {
    Drawer,
    TextField,
    Tooltip,
    MetricCard,
    AttributeRules,
    huxButton,
  },

  props: {
    value: {
      type: Object,
      required: true,
    },

    /**
     * A toggle indicating whether the drawer is open or not.
     */
    toggle: {
      type: Boolean,
      required: false,
      default: false,
    },
  },

  data() {
    return {
      loading: false,
      localToggle: false,
      drawerWidth: 900,
      newAudienceRules: [(v) => !!v || "Audience name is required"],
      newAudienceValidity: false,
      // TODO: need to make API call and update the cards/sizes of metric cards
      newAudience: {
        name: "",
      },
      attributeRules: [],
      infoCards: [
        {
          title: "Size",
          format: "relative",
          helpText:
            "Current number of customers who fit the selected attributes.",
          helpWidth: 232,
          icon: "targetsize",
        },
        {
          title: "Countries",
          value: "1",
          icon: "countries",
        },
        {
          title: "States",
          value: "50",
          helpText:
            "US states or regions equivalent to US state-level (e.g. counties, districts, departments, divisions, parishes, provinces, etc).",
          helpWidth: 283,
          icon: "states",
        },
        {
          title: "Age Range",
          value: "24-68",
          icon: "birth",
        },
        {
          title: "Gender",
          format: "multiple",
          value: "Women",
        },
      ],
    }
  },

  computed: {
    ...mapGetters({
      overview: "customers/overview",
    }),
  },

  watch: {
    toggle(value) {
      this.localToggle = value
    },

    localToggle(value) {
      this.$emit("onToggle", value)
    },
  },

  methods: {
    ...mapActions({
      addAudience: "audiences/add",
      getOverview: "customers/getOverview",
    }),

    closeDrawer() {
      this.localToggle = false
      this.reset()
    },

    onCancelAndBack() {
      this.$emit("onCancelAndBack")
      this.reset()
    },

    getValue(type) {
      switch (type) {
        case "Size":
          return this.overview.total_customers
        case "Age Range":
          return `${this.overview.min_age}-${this.overview.max_age}`
        case "Countries":
          return this.overview.total_countries
        case "States":
          return this.overview.total_us_states
        default:
          // Gender
          return [
            {
              key: "M",
              value: this.overview.gender_men,
            },
            {
              key: "W",
              value: this.overview.gender_women,
            },
            {
              key: "O",
              value: this.overview.gender_other,
            },
          ]
      }
    },

    reset() {
      this.$refs.newAudienceRef.reset()
      this.attributeRules = []
    },

    async add() {
      try {
        this.loading = true
        const filtersArray = []
        for (
          let ruleIndex = 0;
          ruleIndex < this.attributeRules.length;
          ruleIndex++
        ) {
          var filter = {
            section_aggregator: this.attributeRules[ruleIndex].operand
              ? "ALL"
              : "ANY",
            section_filters: [],
          }
          for (
            let conditionIndex = 0;
            conditionIndex < this.attributeRules[ruleIndex].conditions.length;
            conditionIndex++
          ) {
            filter.section_filters.push({
              field:
                this.attributeRules[ruleIndex].conditions[conditionIndex]
                  .attribute.key,
              type: this.attributeRules[ruleIndex].conditions[conditionIndex]
                .operator
                ? this.attributeRules[ruleIndex].conditions[conditionIndex]
                    .operator.key
                : "range",
              value: this.attributeRules[ruleIndex].conditions[conditionIndex]
                .operator
                ? this.attributeRules[ruleIndex].conditions[conditionIndex].text
                : this.attributeRules[ruleIndex].conditions[conditionIndex]
                    .range,
            })
          }
          filtersArray.push(filter)
        }

        const data = {
          name: this.newAudience.name,
          filters: filtersArray,
        }

        const newAudience = await this.addAudience(data)

        this.$set(this.value, newAudience.id, {
          id: newAudience.id,
          name: newAudience.name,
          size: newAudience.size,
          destinations: [],
        })
        this.$emit("onCreateAddAudience", newAudience)
        this.closeDrawer()
      } catch (error) {
        console.error(error)
      } finally {
        this.loading = false
      }
    },
    async fetchDependencies() {
      this.loading = true
      await this.getOverview()
      this.loading = false
    },
  },
}
</script>
<style lang="scss" scoped>
.add-audience-drawer-wrapper {
  .audience-name-field {
    max-width: 360px;
  }
  hr {
    border-style: solid;
  }
}
</style>
