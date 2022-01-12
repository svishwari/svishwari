<template>
  <div class="pt-2">
    <v-card class="overview-card px-6 py-5 card-style">
      <v-card-title class="d-flex justify-space-between pa-0 mb-2">
        <h3 class="text-h3 mb-2">Engagement overview</h3>
        <div class="d-flex align-center">
          <v-btn
            text
            color="primary"
            class="text-body-1 ml-n3 mt-n2"
            data-e2e="delivery-history"
            @click="$emit('openDeliveryHistoryDrawer', $event)"
          >
            <icon
              class="mr-1"
              type="history"
              :size="24"
              :color="'primary'"
              :variant="'base'"
            />
            Delivery history
          </v-btn>
        </div>
      </v-card-title>

      <overview-metric-cards :data="data" />
    </v-card>
    <v-card class="pa-6 card-style mt-6">
      <v-card-title class="d-flex justify-space-between pa-0">
        <h3 class="text-h3 mb-2">
          <icon
            type="audiences"
            :size="24"
            color="black-darken4"
            class="mr-2"
          />
          <span class="p-absolute"
            >Audiences ({{ data.audiences.length }})</span
          >
        </h3>
        <div class="d-flex align-center">
          <v-btn
            text
            color="primary"
            class="text-body-1 ml-n3 mt-n2"
            data-e2e="deliver-all"
            @click="$emit('deliverEngagement', $event)"
          >
            <icon
              class="mr-1"
              type="deliver_2"
              :size="24"
              :color="'primary'"
              :variant="'base'"
            />
            Deliver All
          </v-btn>
        </div>
      </v-card-title>

      <delivery-table
        :section="data"
        audience-key="audiences"
        :filter-tags="filterTags"
        :headers="columnDefs"
        :audience-menu-options="audienceMenuOptions"
        class="audience-table"
        @triggerSelectAudience="$emit('triggerSelectAudience', $event)"
        @onSectionAction="$emit('triggerOverviewAction', $event)"
      />
    </v-card>
  </div>
</template>

<script>
import Icon from "@/components/common/Icon.vue"
import OverviewMetricCards from "./Components/OverviewMetricCards.vue"
import DeliveryTable from "./Components/DeliveryTable.vue"
import { mapGetters } from "vuex"

export default {
  name: "Overview",
  components: { OverviewMetricCards, Icon, DeliveryTable },
  props: {
    data: {
      type: Object,
      required: true,
    },
    loadingAudiences: {
      type: Boolean,
      required: false,
      default: false,
    },
  },
  data() {
    return {
      columnDefs: [
        {
          text: "Audiences",
          value: "name",
          width: "20%",
        },
        {
          text: "Status",
          value: "status",
          width: "15%",
        },
        {
          text: "Destination",
          value: "destinations",
          width: "15%",
        },
        {
          text: "Target size",
          value: "size",
          width: "15%",
          hoverTooltip:
            "Average order value for all customers (known and anyonymous) for all time.",
          tooltipWidth: "201px",
        },
        {
          text: "Attributes",
          value: "filters",
          width: "25%",
        },
        {
          text: "Last delivery",
          value: "update_time",
          width: "10%",
        },
      ],
      audienceMenuOptions: [
        { id: 1, title: "Deliver now", active: true },
        { id: 2, title: "Create lookalike", active: true },
        { id: 3, title: "Add a destination", active: true },
        { id: 4, title: "Remove audience", active: true },
      ],
    }
  },
  computed: {
    ...mapGetters({
      ruleAttributes: "audiences/audiencesRules",
    }),

    filterTags() {
      let filterTagsObj = {}
      let audienceValue = JSON.parse(JSON.stringify(this.data.audiences))
      audienceValue.forEach((audience) => {
        if (audience.filters) {
          filterTagsObj[audience.name] = new Set()
          audience.filters.forEach((item) => {
            item.section_filters.forEach((obj) => {
              let nameObj = this.attributeOptions().find(
                (item) => item.key == obj.field.toLowerCase()
              )
              if (nameObj) {
                filterTagsObj[audience.name].add(nameObj.name)
              }
            })
          })
        }
      })
      return filterTagsObj
    },
  },

  methods: {
    attributeOptions() {
      const options = []
      if (this.ruleAttributes && this.ruleAttributes.rule_attributes) {
        Object.entries(this.ruleAttributes.rule_attributes).forEach((attr) => {
          Object.keys(attr[1]).forEach((optionKey) => {
            if (
              Object.values(attr[1][optionKey])
                .map((o) => typeof o === "object" && !Array.isArray(o))
                .includes(Boolean(true))
            ) {
              Object.keys(attr[1][optionKey]).forEach((att) => {
                if (typeof attr[1][optionKey][att] === "object") {
                  options.push({
                    key: att,
                    name: attr[1][optionKey][att]["name"],
                    category: attr[0],
                  })
                }
              })
            } else {
              options.push({
                key: optionKey,
                name: attr[1][optionKey]["name"],
                category: attr[0],
              })
            }
          })
        })
      }
      return options
    },
  },
}
</script>

<style lang="scss" scoped>
.p-absolute {
  position: absolute !important;
}
.overview-card {
  height: 150px;
}
.audience-table {
  border-radius: 12px;
  border: 1px solid var(--v-black-lighten2);
  overflow: hidden;
  ::v-deep table {
    .v-data-table-header {
      tr {
        th {
          background: var(--v-primary-lighten1);
        }
      }
    }
  }
}
</style>
