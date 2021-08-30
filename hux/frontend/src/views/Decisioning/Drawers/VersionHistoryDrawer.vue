<template>
  <drawer
    v-model="localDrawer"
    :content-padding="'pa-0'"
    :content-header-padding="'px-6'"
  >
    <template #header-left>
      <div class="d-flex align-center">
        <icon type="history" :size="20" color="neroBlack" class="mr-2" />
        <h3 class="text-h3 ml-1 darkGrey--text">Version history</h3>
      </div>
    </template>
    <template #default>
      <v-progress-linear :active="loading" :indeterminate="loading" />
      <hux-data-table
        :columns="columnDefs"
        :sort-column="sortColumn"
        :sort-desc="sortDesc"
        :data-items="versionHistory"
      >
        <template #row-item="{ item }">
          <td
            v-for="header in columnDefs"
            :key="header.value"
            :style="{ width: header.width }"
          >
            <tooltip v-if="header.value == 'version'">
              <span
                class="cell neroBlack--text ml-2"
                :class="[item.current ? 'font-weight-bold' : '']"
              >
                {{ item.version }}
              </span>
              <span class="cell neroBlack--text ml-1">
                {{ item.current && "(Current)" }}
              </span>
              <template #tooltip>
                <div class="my-2 neroBlack--text">
                  Trained date
                  <div class="neroBlack--text">
                    {{ item.trained_date | Date | Empty }}
                  </div>
                </div>
                <div class="my-2 neroBlack--text">
                  Fulcrum date
                  <div class="neroBlack--text">
                    {{ item.fulcrum_date | Date | Empty }}
                  </div>
                </div>
                <div class="my-2 neroBlack--text">
                  Lookback period (Days)
                  <div class="neroBlack--text">
                    {{ item.lookback_window }}
                  </div>
                </div>
                <div class="my-2 neroBlack--text">
                  Prediction period (Days)
                  <div class="neroBlack--text">
                    {{ item.prediction_window }}
                  </div>
                </div>
              </template>
            </tooltip>

            <tooltip v-if="header.value == 'description'">
              <span class="cell neroBlack--text ellipsis-23">
                {{ item.description }}
              </span>
              <template #tooltip>
                <div class="my-2 gray--text">
                  <div class="neroBlack--text">
                    {{ item.description }}
                  </div>
                </div>
              </template>
            </tooltip>

            <div v-if="header.value == 'status'" class="neroBlack--text">
              <status
                :status="item.status"
                :show-label="true"
                class="d-flex"
                :icon-size="17"
              />
            </div>

            <div
              v-if="header.value == 'trained_date'"
              class="cell neroBlack--text"
            >
              <time-stamp :value="item.trained_date" />
            </div>
          </td>
        </template>
      </hux-data-table>
    </template>
    <template #footer-left>
      <tooltip>
        <div class="d-flex align-baseline gray--text text-caption">
          {{ versionHistoryList.length }} results
        </div>
        <template #tooltip> {{ versionHistoryList.length }} results </template>
      </tooltip>
    </template>
  </drawer>
</template>

<script>
import { mapActions, mapGetters } from "vuex"
import HuxDataTable from "@/components/common/dataTable/HuxDataTable.vue"
import Drawer from "@/components/common/Drawer"
import Tooltip from "@/components/common/Tooltip"
import TimeStamp from "@/components/common/huxTable/TimeStamp.vue"
import Status from "@/components/common/Status.vue"
import Icon from "@/components/common/Icon.vue"

export default {
  name: "VersionHistory",
  components: {
    Drawer,
    Tooltip,
    HuxDataTable,
    TimeStamp,
    Status,
    Icon,
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
      localDrawer: this.value,
      sortColumn: "version",
      sortDesc: true,
      columnDefs: [
        {
          text: "Version",
          value: "version",
          width: "160px",
        },
        {
          text: "Description",
          value: "description",
          width: "auto",
        },
        {
          text: "Status",
          value: "status",
          width: "116px",
        },
        {
          text: "Trained date",
          value: "trained_date",
          width: "140px",
        },
      ],
    }
  },

  computed: {
    ...mapGetters({
      versionHistoryList: "models/history",
    }),

    versionHistory() {
      let sortedVersionHistoryList = this.versionHistoryList
      return sortedVersionHistoryList.sort((a, b) => a.version - b.version)
    },
  },

  watch: {
    value: function () {
      this.localDrawer = this.value
      if (this.localDrawer) {
        this.loading = true
        this.getHistory(this.$route.params.id)
        this.loading = false
      }
    },
    localDrawer: function () {
      this.$emit("input", this.localDrawer)
    },
  },

  methods: {
    ...mapActions({
      getHistory: "models/getHistory",
    }),
  },
}
</script>
<style lang="scss" scoped>
.hux-data-table {
  ::v-deep table {
    .v-data-table-header {
      tr {
        height: 40px !important;
      }
      th {
        background: var(--v-aliceBlue-base);
      }
      th:nth-child(1) {
        padding-left: 24px;
      }
    }
    tr {
      td {
        height: 40px !important;
        padding-top: 4px !important;
        padding-bottom: 4px !important;
      }
    }
    .cell {
      font-family: Open Sans;
      font-style: normal;
      font-weight: normal;
      font-size: 14px !important;
      display: inline-block;
      max-width: 100%;
      overflow: hidden;
      text-decoration: none;
    }
  }
  .ellipsis-23 {
    overflow: hidden;
    text-overflow: ellipsis;
    max-width: 23ch;
    display: inline-block;
    width: 23ch;
    white-space: nowrap;
  }
}
</style>
