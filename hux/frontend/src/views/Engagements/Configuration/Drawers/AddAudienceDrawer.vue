<template>
  <drawer
    v-model="localToggle"
    class="add-audience-drawer-wrapper"
    :width="drawerWidth"
    :loading="loading"
    @onClose="closeDrawer()"
    @iconToggle="changeOverviewListItems"
  >
    <template #header-left>
      <h3 class="text-h3">Create a new audience</h3>
    </template>

    <template #default>
      <div class="pa-4">
        <h6 class="pb-6 text-h6 black--text text--darken-4">
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
        <div class="pt-4 pb-2 black--text text--darken-4 text-caption">
          Audience overview
        </div>
        <div class="d-flex align-center pb-4">
          <metric-card
            v-for="(item, i) in overviewListItems"
            :key="i"
            class="list-item ma-0 mr-3"
            :class="{ 'd-none': i > overviewListItems.length - 3 && !expanded }"
            :title="item.title"
          >
            <template #subtitle-extended>
              <tooltip>
                <template #label-content>
                  <span class="font-weight-semi-bold">
                    {{ getFormattedValue(item) }}
                  </span>
                </template>
                <template #hover-content>
                  {{ item.subtitle | Numeric | Empty }}
                </template>
              </tooltip>
            </template>
          </metric-card>
        </div>
        <hr class="black-lighten2 mb-4" />
        <div class="pt-1 pr-0">
          <attribute-rules
            :rules="attributeRules"
            apply-caption-style
            enable-title
            @updateOverview="(data) => mapCDMOverview(data)"
          />
        </div>
      </div>
    </template>

    <template #footer-left>
      <v-btn tile color="white" @click="onCancelAndBack()">
        <span class="primary--text">Cancel &amp; back</span>
      </v-btn>
      <v-btn
        :disabled="!newAudienceValidity"
        tile
        color="primary"
        @click="add()"
      >
        Create &amp; add
      </v-btn>
    </template>
  </drawer>
</template>

<script>
import { mapGetters, mapActions } from "vuex"
import Drawer from "@/components/common/Drawer.vue"
import TextField from "@/components/common/TextField"
import MetricCard from "@/components/common/MetricCard"
import AttributeRules from "@/views/Audiences/AttributeRules"
import Tooltip from "@/components/common/Tooltip"

export default {
  name: "AddAudienceDrawer",

  components: {
    Drawer,
    TextField,
    Tooltip,
    MetricCard,
    AttributeRules,
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
      overviewListItems: [
        { title: "Target size", subtitle: "" },
        { title: "Countries", subtitle: "" },
        { title: "US States", subtitle: "" },
        { title: "Cities", subtitle: "" },
        { title: "Age", subtitle: "" },
        { title: "Women", subtitle: "" },
        { title: "Men", subtitle: "" },
        { title: "Other", subtitle: "" },
      ],
      attributeRules: [],
      expanded: false,
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

    changeOverviewListItems(expanded) {
      this.expanded = expanded
    },

    // Mapping Overview Data
    mapCDMOverview(data) {
      this.overviewListItems[0].subtitle = data.total_customers
      this.overviewListItems[1].subtitle = data.total_countries
      this.overviewListItems[2].subtitle = data.total_us_states
      this.overviewListItems[3].subtitle = data.total_cities
      let min_age = data.min_age
      let max_age = data.max_age
      if (min_age && max_age && min_age === max_age) {
        this.overviewListItems[4].subtitle = min_age
      } else if (min_age && max_age) {
        this.overviewListItems[4].subtitle = `${min_age}-${max_age}`
      } else {
        this.overviewListItems[4].subtitle = "-"
      }
      this.overviewListItems[5].subtitle = data.gender_women
      this.overviewListItems[6].subtitle = data.gender_men
      this.overviewListItems[7].subtitle = data.gender_other
    },

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
          return this.$options.filters.Percentage(item.subtitle)
        default:
          return item.subtitle
      }
    },

    reset() {
      this.$refs.newAudienceRef.reset()
      this.attributeRules = []
      this.expanded = false
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
      this.mapCDMOverview(this.overview)
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
