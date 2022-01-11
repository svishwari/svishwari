<template>
  <drawer
    v-model="localDrawer"
    :content-padding="'pa-0'"
    :content-header-padding="'px-4'"
  >
    <template #header-left>
      <div class="d-flex align-center">
        <icon type="version-history" :size="32" class="mr-2" />
        <h3 class="text-h2 ml-1 black--text">Version history</h3>
      </div>
    </template>
    <template #default>
      <v-progress-linear :active="loading" :indeterminate="loading" />
      <hux-data-table
        v-if="!loading"
        :columns="columnDefs"
        :data-items="versionHistory"
        sort-column="trained_date"
        sort-desc="true"
      >
        <template #row-item="{ item }">
          <td
            v-for="header in columnDefs"
            :key="header.value"
            :style="{ width: header.width }"
            class="pr-0"
          >
            <tooltip v-if="header.value == 'version'">
              <span
                class="cell black--text text-body-1 ml-2"
                :class="[item.current ? 'font-weight-bold' : '']"
              >
                {{ item.version }}
              </span>
              <span class="cell black--text text-body-1 ml-1">
                {{ item.current && "(Current)" }}
              </span>
              <template #tooltip>
                <div class="my-2 black--text text-body-2">
                  Trained date
                  <div class="black--text text-body-2">
                    {{ item.trained_date | Date | Empty }}
                  </div>
                </div>
                <div class="my-2 black--text text-body-2">
                  Fulcrum date
                  <div class="black--text text-body-2">
                    {{ item.fulcrum_date | Date | Empty }}
                  </div>
                </div>
                <div class="my-2 black--text text-body-2">
                  Lookback period (Days)
                  <div class="black--text text-body-2">
                    {{ item.lookback_window }}
                  </div>
                </div>
                <div class="my-2 black--text text-body-2">
                  Prediction period (Days)
                  <div class="black--text text-body-2">
                    {{ item.prediction_window }}
                  </div>
                </div>
              </template>
            </tooltip>

            <tooltip v-if="header.value == 'description'">
              <span class="cell black--text text-body-1 ellipsis-23">
                {{ item.description }}
              </span>
              <template #tooltip>
                <div class="my-2 black--text text-body-2">
                  <div class="black--text text-body-2">
                    {{ item.description }}
                  </div>
                </div>
              </template>
            </tooltip>

            <div
              v-if="header.value == 'status'"
              class="black--text text-body-1"
            >
              <status
                :status="item.status"
                :show-label="true"
                class="d-flex"
                :icon-size="17"
              />
            </div>

            <div
              v-if="header.value == 'trained_date'"
              class="cell black--text text-body-1"
            >
              <time-stamp :value="item.trained_date" />
            </div>
          </td>
        </template>
      </hux-data-table>
    </template>
    <template #footer-left>
      <tooltip>
        <div
          class="d-flex align-baseline black--text text--lighten-4 text-body-2"
        >
          {{ versionHistoryList.length }} results
        </div>
        <template #tooltip>
          <span class="text-body-1 black-text"
            >{{ versionHistoryList.length }} results
          </span></template
        >
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
      columnDefs: [
        {
          text: "Version",
          value: "version",
          width: "180px",
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
      return this.versionHistoryList
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
        background: var(--v-primary-lighten2) !important;
        padding-left: 0px !important;
      }
      th:nth-child(1) {
        padding-left: 24px;
      }
      th:first-child {
        padding-left: 33px !important;
      }
    }
    tr {
      td {
        height: 40px !important;
        padding-top: 4px !important;
        padding-bottom: 4px !important;
        padding-left: 0px !important;
      }
    }

    tr:nth-child(1) {
      background: var(--v-primary-lighten1);
      box-shadow: 4px 4px 10px var(--v-black-lighten3);
    }

    td:first-child {
      padding-left: 25px !important;
    }

    .cell {
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
