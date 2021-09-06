<template>
  <drawer v-model="localToggle" content-padding="pa-0">
    <template #header-left>
      <div class="d-flex align-center">
        <icon
          type="history"
          :size="20"
          color="var(--v-black-darken4)"
          class="mr-4"
        />
        <h3 class="text-h3">Delivery history</h3>
      </div>
    </template>

    <template #default>
      <v-progress-linear :active="loading" :indeterminate="loading" />

      <hux-data-table
        :columns="columns"
        :data-items="items"
        sort-column="delivered"
        class="delivery-list"
      >
        <template #row-item="{ item }">
          <td
            v-for="(col, index) in columns"
            :key="index"
            :style="{ width: col.width }"
            class="text-body-1"
          >
            <tooltip>
              <router-link
                v-if="['audience', 'engagement'].includes(col.value)"
                :to="{
                  name:
                    col.value === 'audience'
                      ? 'AudienceInsight'
                      : 'EngagementDashboard',
                  params: { id: item[col.value].id },
                }"
                class="d-inline-block mw-100 text-truncate text-decoration-none"
              >
                {{ item[col.value].name }}
              </router-link>
              <template #tooltip>
                {{ item[col.value].name }}
              </template>
            </tooltip>
            <tooltip v-if="col.value === 'destination' && item[col.value]">
              <template #label-content>
                <logo
                  :key="item[col.value].type"
                  :type="item[col.value].type"
                  :size="18"
                  class="mb-0"
                >
                </logo>
              </template>
              <template #hover-content>
                {{ item[col.value].name }}
              </template>
            </tooltip>
            <tooltip v-if="col.value === 'size'">
              <template #label-content>
                {{ item[col.value] | Numeric(true, true) }}
              </template>
              <template #hover-content>
                {{ item[col.value] | Numeric(true) }}
              </template>
            </tooltip>
            <tooltip v-if="col.value === 'match_rate'">
              <template #label-content>
                {{ item[col.value] | Percentage }}
              </template>
              <template #hover-content>
                {{ item[col.value] }}
              </template>
            </tooltip>
            <tooltip v-if="col.value === 'delivered'">
              <template #label-content>
                {{ item[col.value] | Date("relative") }}
              </template>
              <template #hover-content>
                {{ item[col.value] | Date }}
              </template>
            </tooltip>
          </td>
        </template>
      </hux-data-table>
    </template>

    <template #footer-left>
      <span class="black--text text--darken-1 text-caption"
        >{{ items.length }} results</span
      >
    </template>
  </drawer>
</template>

<script>
import { mapActions, mapGetters } from "vuex"
import HuxDataTable from "@/components/common/dataTable/HuxDataTable.vue"
import Drawer from "@/components/common/Drawer.vue"
import Icon from "@/components/common/Icon.vue"
import Logo from "@/components/common/Logo.vue"
import Tooltip from "@/components/common/Tooltip.vue"

export default {
  name: "DeliveryHistoryDrawer",

  components: {
    HuxDataTable,
    Drawer,
    Icon,
    Logo,
    Tooltip,
  },

  props: {
    audienceId: {
      required: false,
      default: null,
    },

    engagementId: {
      required: false,
      default: null,
    },

    toggle: {
      type: Boolean,
      required: false,
      default: false,
    },
  },

  data() {
    return {
      localToggle: false,
      loading: false,
      columns: [
        {
          value: "destination",
          text: "Destination",
          width: "113px",
        },
        {
          value: "size",
          text: "Target size",
          width: "108px",
        },
        {
          value: "match_rate",
          text: "Match Rate",
          width: "111px",
        },
        {
          value: "delivered",
          text: "Delivered",
          width: "114px",
        },
      ],
    }
  },

  computed: {
    ...mapGetters({
      audienceDeliveries: "audiences/deliveries",
      engagementDeliveries: "engagements/deliveries",
      getDestination: "destinations/single",
    }),

    items() {
      if (this.audienceId) return this.audienceDeliveries(this.audienceId)
      else return this.engagementDeliveries(this.engagementId)
    },
  },

  watch: {
    toggle(value) {
      this.localToggle = value
    },

    localToggle(value) {
      this.$emit("onToggle", value)
    },
  },

  async updated() {
    if (this.toggle) {
      await this.fetchHistory()
    }
  },

  mounted() {
    if (this.engagementId !== null)
      this.columns.unshift({
        value: "audience",
        text: "Audience name",
        width: "35%",
      })

    if (this.audienceId !== null)
      this.columns.unshift({
        value: "engagement",
        text: "Engagement name",
        width: "35%",
      })
  },

  methods: {
    ...mapActions({
      getAudienceDeliveries: "audiences/getDeliveries",
      getEngagementDeliveries: "engagements/getDeliveries",
    }),

    async fetchHistory() {
      this.loading = true

      if (this.engagementId)
        await this.getEngagementDeliveries(this.engagementId)

      if (this.audienceId) await this.getAudienceDeliveries(this.audienceId)

      this.loading = false
    },
  },
}
</script>
