<template>
  <drawer v-model="localToggle" content-padding="pa-0">
    <template #header-left>
      <h3 v-if="dataFeed" class="text-h3">
        {{ dataFeed.datafeed_name }} – {{ dataFeed.last_run | Date }}
      </h3>
    </template>

    <template #default>
      <v-progress-linear :active="loading" :indeterminate="loading" />

      <v-expansion-panels
        v-if="!loading"
        flat
        tile
        multiple
        accordion
        :value="[0, 1]"
      >
        <v-expansion-panel
          v-for="(reportKey, i) in Object.keys(reports)"
          :key="i"
        >
          <v-expansion-panel-header
            class="panel-header"
            :data-e2e="reportNames[reportKey]"
          >
            <template #actions>
              <v-icon color="blue"> $expand </v-icon>
            </template>
            <h5 class="text-h5 blue--text">
              {{ reportNames[reportKey] }}
            </h5>
          </v-expansion-panel-header>

          <v-expansion-panel-content class="panel-content">
            <hux-data-table :columns="columns" :data-items="reports[reportKey]">
              <template #row-item="{ item }">
                <td
                  v-for="(col, index) in columns"
                  :key="index"
                  :style="{ width: col.width }"
                  class="text-body-2"
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
          </v-expansion-panel-content>
        </v-expansion-panel>
      </v-expansion-panels>
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
</style>
