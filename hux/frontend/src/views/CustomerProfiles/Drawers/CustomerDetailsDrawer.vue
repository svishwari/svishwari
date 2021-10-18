<template>
  <drawer
    v-model="localDrawer"
    :content-padding="'pa-0'"
    :content-header-padding="'px-3'"
  >
    <template #header-left>
      <div class="d-flex align-center">
        <h3 class="text-h3 ml-1 black--text text--darken-4">Customers</h3>
      </div>
    </template>

    <template #default>
      <v-progress-linear :active="loading" :indeterminate="loading" />
      <hux-data-table
        v-if="!loading"
        :columns="columnDefs"
        :sort-column="'hux_id'"
        :data-items="customers"
      >
        <template #row-item="{ item }">
          <td
            v-for="header in columnDefs"
            :key="header.value"
            :style="{ width: header.width }"
          >
            <tooltip v-if="header.value == 'hux_id'">
              <router-link
                :to="{
                  name: 'CustomerProfileDetails',
                  params: { id: item[header.value] },
                }"
                data-e2e="customerID"
                class="cell"
                append
              >
                {{ item[header.value] }}
              </router-link>
              <template #tooltip>
                <div class="my-2 black--text text--darken-1">
                  Hux ID:
                  <span class="black--text text--darken-4">
                    {{ item[header.value] }}
                  </span>
                </div>
                <div class="my-2 black--text text--darken-1">
                  Full name:
                  <span class="black--text text--darken-4">
                    {{ item.last_name }}, {{ item.first_name }}
                  </span>
                </div>
                <div class="my-2 black--text text--darken-1">
                  Match confidence:
                  <span class="black--text text--darken-4">
                    {{
                      item.match_confidence | Numeric(true, false, false, true)
                    }}
                  </span>
                </div>
              </template>
            </tooltip>
            <div
              v-if="header.value == 'first_name' || header.value == 'last_name'"
              class="cell"
            >
              <span v-if="item.last_name">{{ item.last_name }}, </span>
              <span v-if="item.first_name"> {{ item.first_name }}</span>
            </div>
            <div v-if="header.value == 'match_confidence'">
              <hux-slider
                :is-range-slider="false"
                :value="item[header.value]"
                class="match-confidence"
              ></hux-slider>
            </div>
          </td>
        </template>
      </hux-data-table>
      <v-progress-linear v-if="enableLazyLoad" active indeterminate />
      <observer v-if="customers.length" @intersect="intersected"></observer>
    </template>
    <template #footer-left>
      <tooltip>
        <div
          class="
            d-flex
            align-baseline
            footer-font
            black--text
            text--darken-1 text-caption
          "
        >
          {{ customerOverview.total_customers | Numeric(true, true) }} results
        </div>
        <template #tooltip>
          {{ customerOverview.total_customers | Numeric(true, false, false) }}
          results
        </template>
      </tooltip>
    </template>
  </drawer>
</template>

<script>
import { mapActions, mapGetters } from "vuex"
import Drawer from "@/components/common/Drawer"
import HuxDataTable from "@/components/common/dataTable/HuxDataTable.vue"
import HuxSlider from "@/components/common/HuxSlider"
import Tooltip from "@/components/common/Tooltip"
import Observer from "@/components/common/Observer"

export default {
  name: "CustomerDetails",
  components: {
    Drawer,
    HuxDataTable,
    HuxSlider,
    Tooltip,
    Observer,
  },

  props: {
    value: {
      type: Boolean,
      required: true,
      default: false,
    },
  },
  data() {
    return {
      loading: true,
      enableLazyLoad: false,
      localDrawer: this.value,
      batchCount: 1,
      columnDefs: [
        {
          text: "Hux ID",
          value: "hux_id",
          width: "auto",
        },
        {
          text: "Full name",
          value: "first_name",
          width: "auto",
        },
        {
          text: "Match confidence",
          value: "match_confidence",
          width: "200px",
          hoverTooltip:
            "A percentage that indicates the level of certainty that all incoming records were accurately matched to a given customer.",
        },
      ],
      lastBatch: 0,
      batchDetails: {
        batchSize: 100,
        batchNumber: 1,
        isLazyLoad: false,
      },
    }
  },

  computed: {
    ...mapGetters({
      customersList: "customers/list",
      customerOverview: "customers/overview",
    }),

    customers() {
      let sortedCustomerList = this.customersList
      return sortedCustomerList.sort((a, b) => a.id - b.id)
    },
  },

  watch: {
    value: function () {
      this.localDrawer = this.value
    },
    localDrawer: function () {
      this.$emit("input", this.localDrawer)
    },
  },

  async updated() {
    if (this.localDrawer) {
      this.loading = true
      await this.fetchCustomerByBatch()
      this.calculateLastBatch()
      this.loading = false
      this.enableLazyLoad = true
    } else {
      this.batchDetails.batchNumber = 1
      this.batchDetails.isLazyLoad = false
      this.enableLazyLoad = false
    }
  },

  methods: {
    ...mapActions({
      getCustomers: "customers/getAll",
    }),
    async fetchCustomerByBatch() {
      await this.getCustomers(this.batchDetails)
      this.batchDetails.batchNumber++
    },
    intersected() {
      if (this.batchDetails.batchNumber <= this.lastBatch) {
        this.batchDetails.isLazyLoad = true
        this.fetchCustomerByBatch()
      } else {
        this.enableLazyLoad = false
      }
    },
    calculateLastBatch() {
      this.lastBatch = Math.ceil(
        this.customerOverview.total_customers / this.batchDetails.batchSize
      )
    },
  },
}
</script>

<style lang="scss" scoped>
.hux-data-table {
  margin-top: 1px;
}
::v-deep .v-sheet .theme--light .v-toolbar {
  background: var(--v-primary-lighten2);
}
::v-deep .theme--light.v-sheet {
  box-shadow: 0px 1px 5px rgba(0, 0, 0, 0.25);
}
::v-deep .hux-data-table {
  .v-data-table {
    .v-data-table-header {
      tr {
        height: 40px !important;
      }
      th {
        background: var(--v-primary-lighten2);
      }
    }
    > .v-data-table__wrapper {
      > table {
        > tbody > tr > td {
          padding-top: 0;
          padding-bottom: 0;
        }
      }
    }
    .match-confidence {
      .slider-value-display {
        margin-top: 16px;
      }
      .v-slider__track-container {
        margin-top: 12px !important;
      }
      .v-slider__thumb-container {
        margin-top: 12px !important;
      }
    }
  }
  .cell {
    font-family: Open Sans;
    font-style: normal;
    font-weight: normal;
    font-size: 14px !important;
    line-height: 22px;
    display: inline-block;
    max-width: 100%;
    overflow: hidden;
    text-decoration: none;
    text-overflow: ellipsis;
  }
}
.footer-font {
  color: var(--v-black-darken1);
}
</style>
