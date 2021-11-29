<template>
  <drawer v-model="localToggle" content-padding="pa-0">
    <template #header-left>
      <h2 v-if="dataFeed" class="text-h2 truncate">
        {{ dataFeed.datafeed_name }}
      </h2>
      <h2 v-if="dataFeed" class="text-h2">
        – {{ dataFeed.last_run | Date((format = "M/D/YYYY h:mm a")) }}
      </h2>
    </template>

    <template #default>
      <v-progress-linear :active="loading" :indeterminate="loading" />

      <v-tabs v-model="tabOption" class="mt-2">
        <v-tabs-slider color="primary"></v-tabs-slider>
        <div class="d-flex">
          <v-tab
            v-for="(reportKey, i) in Object.keys(reports)"
            :key="i"
            class="pa-2 mr-3 text-h3 black--text text--lighten-4"
            data-e2e="last-run-tab"
          >
            {{ reportNames[reportKey] }}
          </v-tab>
        </div>
      </v-tabs>
      <v-tabs-items v-model="tabOption" class="mt-2">
        <v-tab-item v-for="(reportKey, i) in Object.keys(reports)" :key="i">
          <hux-data-table :columns="columns" :data-items="reports[reportKey]">
            <template #row-item="{ item }">
              <td
                v-for="(col, index) in columns"
                :key="index"
                :style="{ width: col.width }"
                class="text-body-1"
              >
                <template v-if="col.value === 'result'">
                  <template v-if="resultAsPercentage.includes(item.metric)">
                    {{
                      item[col.value]
                        | Numeric(false, false, false, (percentage = true))
                    }}
                  </template>
                  <template v-else-if="resultAsDate.includes(item.metric)">
                    {{ item[col.value] | Date }}
                  </template>
                  <template
                    v-else-if="item.metric === 'Process time in seconds'"
                  >
                    {{ item[col.value] }} second(s)
                  </template>
                  <template v-else>
                    {{ item[col.value] }}
                  </template>
                </template>
                <template v-else>
                  {{ item[col.value] }}
                </template>
              </td>
            </template>
          </hux-data-table>
        </v-tab-item>
      </v-tabs-items>
    </template>
  </drawer>
</template>

<script>
import { mapActions, mapGetters } from "vuex"
import HuxDataTable from "@/components/common/dataTable/HuxDataTable.vue"
import Drawer from "@/components/common/Drawer.vue"

export default {
  name: "DestinationsDrawer",

  components: {
    HuxDataTable,
    Drawer,
  },

  props: {
    value: {
      type: Boolean,
      required: true,
      default: false,
    },

    dataFeedId: {
      required: true,
    },
  },

  data() {
    return {
      localToggle: false,
      loading: false,
      columns: [
        {
          value: "metric",
          text: "Metrics",
          width: "250px",
        },
        {
          value: "result",
          text: "Results",
          width: "auto",
        },
      ],
      reportNames: {
        pinning: "Pinning",
        stitched: "Stitched",
      },
      resultAsDate: ["Date & time", "Time stamp"],
      resultAsPercentage: ["Merge rate", "Match rate"],
      tabOption: 0,
    }
  },

  computed: {
    ...mapGetters({
      dataFeedReport: "identity/dataFeedReport",
      dataFeedById: "identity/dataFeed",
    }),

    dataFeed() {
      return this.dataFeedById(this.dataFeedId)
    },

    reports() {
      return this.dataFeedReport(this.dataFeedId) || {}
    },
  },

  watch: {
    value: function () {
      this.localToggle = this.value
    },

    localToggle: function () {
      this.$emit("input", this.localToggle)
    },
  },

  async updated() {
    await this.fetchDataFeedReport()
  },

  methods: {
    ...mapActions({
      getDataFeedReport: "identity/getDataFeedReport",
    }),

    async fetchDataFeedReport() {
      this.loading = true
      try {
        await this.getDataFeedReport(this.dataFeedId)
      } finally {
        this.loading = false
      }
    },
  },
}
</script>

<style lang="scss" scoped>
::v-deep .v-data-table > .v-data-table__wrapper > table > thead > tr > th {
  background: var(--v-primary-lighten2) !important;
  padding-top: 13px;
  padding-bottom: 13px;
}

.panel-content {
  ::v-deep .v-expansion-panel-content__wrap {
    padding: 0;
  }
}

.panel-header {
  border-bottom-width: 1px;
  border-bottom-style: solid;
  border-color: var(--v-primary-lighten3);
  flex-direction: row-reverse;
  height: 40px;

  ::v-deep .v-expansion-panel-header__icon {
    margin-left: 0;
    margin-right: 8px;
  }
}

::v-deep .v-expansion-panel--active {
  > .v-expansion-panel-header--active {
    .v-expansion-panel-header__icon:not(.v-expansion-panel-header__icon--disable-rotate) {
      .v-icon {
        @extend .rotate-icon-0;
      }
    }
  }
}

::v-deep .v-expansion-panels {
  .v-expansion-panel-header {
    .v-expansion-panel-header__icon {
      .v-icon {
        @extend .rotate-icon-n90;
      }
    }
  }
}

::v-deep .v-data-table {
  > .v-data-table__wrapper {
    > table {
      > thead,
      > tbody,
      > tfoot {
        tr {
          td {
            height: 40px;
          }
        }
      }
    }
  }
}

::v-deep .v-tabs .v-tabs-bar .v-tabs-bar__content .v-tab {
  color: var(--v-black-lighten4) !important;
}

.truncate {
  width: 281px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
::v-deep .v-toolbar__title {
  display: inline-flex !important;
}

::v-deep .v-toolbar__content {
  padding: 16px 62px 20px 20px;
}
</style>
