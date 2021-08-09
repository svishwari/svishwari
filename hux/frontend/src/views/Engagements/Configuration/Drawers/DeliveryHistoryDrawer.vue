<template>
  <drawer v-model="localToggle" content-padding="pa-0">
    <template #header-left>
      <div class="d-flex align-center">
        <icon type="history" :size="20" color="neroBlack" class="mr-4" />
        <h3 class="text-h3">Delivery history</h3>
      </div>
    </template>

    <template #default>
      <v-progress-linear :active="loading" :indeterminate="loading" />

      <hux-data-table
        :columns="headers"
        :data-items="items"
        sort-column="delivered"
      >
        <template #row-item="{ item }">
          <td
            v-for="(header, index) in headers"
            :key="index"
            :style="{ width: header.width }"
            class="text-body-1"
          >
            <tooltip>
              <router-link
                v-if="header.value === 'audience'"
                :to="{
                  name: 'AudienceInsight',
                  params: { id: item.audience.id },
                }"
                class="d-inline-block mw-100 text-truncate text-decoration-none"
              >
                {{ item.audience.name }}
              </router-link>
              <template #tooltip>
                {{ item.audience.name }}
              </template>
            </tooltip>
            <tooltip
              v-if="header.value === 'destination' && item[header.value]"
            >
              <template #label-content>
                <logo
                  :key="item[header.value].type"
                  :type="item[header.value].type"
                  :size="18"
                  class="mb-0"
                >
                </logo>
              </template>
              <template #hover-content>
                {{ item[header.value].name }}
              </template>
            </tooltip>
            <tooltip v-if="header.value === 'size'">
              <template #label-content>
                {{ item[header.value] | Numeric(true, true) }}
              </template>
              <template #hover-content>
                {{ item[header.value] | Numeric(true) }}
              </template>
            </tooltip>
            <tooltip v-if="header.value === 'delivered'">
              <template #label-content>
                {{ item[header.value] | Date("relative") }}
              </template>
              <template #hover-content>
                {{ item[header.value] | Date }}
              </template>
            </tooltip>
          </td>
        </template>
      </hux-data-table>
    </template>

    <template #footer-left>
      <span class="gray--text text-caption">{{ items.length }} results</span>
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
    engagementId: {
      required: true,
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
      headers: [
        {
          value: "audience",
          text: "Audience name",
          width: "35%",
        },
        {
          value: "destination",
          text: "Destination",
          width: "20%",
        },
        {
          value: "size",
          text: "Target size",
          width: "18%",
        },
        {
          value: "delivered",
          text: "Delivered",
          width: "27%",
        },
      ],
    }
  },

  computed: {
    ...mapGetters({
      engagementDeliveries: "engagements/deliveries",
      getDestination: "destinations/single",
    }),

    items() {
      return this.engagementDeliveries(this.engagementId)
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

  methods: {
    ...mapActions({
      getEngagementDeliveries: "engagements/getDeliveries",
    }),

    async fetchHistory() {
      this.loading = true
      await this.getEngagementDeliveries(this.engagementId)
      this.loading = false
    },
  },
}
</script>

<style lang="scss" scoped>
::v-deep .v-data-table > .v-data-table__wrapper > table > thead > tr > th {
  background: var(--v-aliceBlue-base) !important;
  padding-top: 13px;
  padding-bottom: 13px;
}
</style>
