<template>
  <div class="models-wrap">
    <div
      class="d-flex flex-nowrap align-stretch flex-grow-1 flex-shrink-0 mw-100"
    >
      <div class="flex-grow-1 flex-shrink-1 overflow-hidden mw-100">
        <v-row class="pb-7 pl-3 white">
          <hux-lazy-data-table
            :columns="columnDefs"
            :data-items="modelsData"
            sort-column="name"
            sort-desc
            class="big-table mt-2"
            data-e2e="models-table"
            view-height="calc(100vh - 265px)"
          >
            <template #row-item="{ item }">
              <td
                v-for="header in columnDefs"
                :key="header.value"
                :class="{
                  'fixed-column': header.fixed,
                  'v-data-table__divider': header.fixed,
                  'primary--text': header.fixed,
                }"
                class="col-overflow text-body-1"
                :style="{ width: header.width, left: 0 }"
              >
                <div v-if="header.value == 'name'">
                  <a data-e2e="model-name-click" @click="goToDashboard(item)">
                    <tooltip>
                      <template #label-content>
                        <logo
                          :key="item.name"
                          :size="18"
                          class="mr-1"
                          :type="`model-${getModelType(item)}`"
                        />
                        {{ item[header.value] | Empty("-") }}
                      </template>
                      <template #hover-content>
                        {{ item[header.value] | Empty("-") }}
                      </template>
                    </tooltip>
                  </a>
                </div>
                <div v-if="header.value == 'status'">
                  <tooltip>
                    <template #label-content>
                      <status
                        :status="item[header.value]"
                        :show-label="true"
                        class="d-flex"
                        :icon-size="18"
                      />
                    </template>
                    <template #hover-content>
                      <status
                        :status="item[header.value]"
                        :show-label="true"
                        class="d-flex"
                        :icon-size="18"
                      />
                    </template>
                  </tooltip>
                </div>

                <div v-if="header.value == 'description'" max-width="59%">
                  <tooltip>
                    <template #label-content>
                      {{ formatText(item["description"]) | Empty("-") }}
                    </template>
                    <template #hover-content>
                      {{ formatText(item["description"]) | Empty("-") }}
                    </template>
                  </tooltip>
                </div>

                <tooltip v-if="header.value == 'category'">
                  <template #label-content>
                    <v-chip
                      small
                      class="mr-1 ml-0 mt-0 mb-1 text-subtitle-2"
                      text-color="primary"
                      color="var(--v-primary-lighten3)"
                    >
                      {{ formatText(item[header.value]) }}
                    </v-chip>
                  </template>
                  <template #hover-content>
                    {{ formatText(item[header.value]) | Empty("-") }}
                  </template>
                </tooltip>

                <div v-if="header.value == 'tags'">
                  <div
                    v-if="
                      item[header.value] &&
                      item[header.value].industry.length > 0
                    "
                    class="d-flex align-center"
                  >
                    <div class="d-flex align-center destination-ico">
                      <tooltip
                        v-for="tag in item[header.value].industry"
                        :key="`${item.id}-${tag}`"
                      >
                        <template #label-content>
                          <logo
                            :key="tag"
                            :size="18"
                            class="mr-1"
                            :type="`${tag}_logo`"
                          />
                        </template>
                        <template #hover-content>
                          <span>{{ formatText(tag) }}</span>
                        </template>
                      </tooltip>
                    </div>
                  </div>
                  <span v-else>—</span>
                </div>
                <tooltip
                  v-if="header.value == 'latest_version'"
                  max-width="47%"
                >
                  <template #label-content>
                    {{ item[header.value] }}
                  </template>
                  <template #hover-content>
                    {{ item[header.value] | Empty("-") }}
                  </template>
                </tooltip>

                <div v-if="header.value == 'last_trained'">
                  <time-stamp :value="item['last_trained']" />
                </div>
              </td>
            </template>
          </hux-lazy-data-table>
        </v-row>
      </div>
    </div>
  </div>
</template>

<script>
import { formatText } from "@/utils"
import HuxLazyDataTable from "@/components/common/dataTable/HuxLazyDataTable.vue"
import Tooltip from "@/components/common/Tooltip.vue"
import Status from "@/components/common/Status.vue"
import Logo from "@/components/common/Logo.vue"
import TimeStamp from "@/components/common/huxTable/TimeStamp.vue"

export default {
  name: "ModelTable",
  components: {
    HuxLazyDataTable,
    Tooltip,
    Status,
    Logo,
    TimeStamp,
  },
  props: {
    sourceData: {
      type: Array,
      required: true,
    },
  },
  data() {
    return {
      columnDefs: [
        {
          text: "Model Name",
          value: "name",
          width: "320px",
        },
        {
          text: "Status",
          value: "status",
          width: "136px",
        },
        {
          text: "Description",
          value: "description",
          width: "410px",
        },
        {
          text: "Category",
          value: "category",
          width: "168px",
        },
        {
          text: "Industry",
          value: "tags",
          width: "220px",
        },
        {
          text: "Version",
          value: "latest_version",
          width: "200px",
        },
        {
          text: "Last trained",
          value: "last_trained",
          width: "200px",
        },
      ],
      modelTypes: [
        "purchase",
        "prediction",
        "ltv",
        "churn",
        "propensity",
        "unsubscribe",
        "regression",
        "classification",
      ],
      sortColumn: "id",
      sortDesc: true,
    }
  },
  computed: {
    modelsData() {
      let sortedModelslist = this.sourceData
      return sortedModelslist.sort((a, b) => a.id - b.id)
    },
  },
  methods: {
    goToDashboard(model) {
      if (model.status === "Active") {
        this.$router.push({
          name: "ModelDashboard",
          params: {
            id: model.id,
            name: model.name,
            type: model.type,
          },
        })
      }
    },
    getModelType(model) {
      return this.modelTypes.includes(
        model.type ? model.type.toLowerCase() : ""
      )
        ? model.type.toLowerCase()
        : "unknown"
    },
    formatText: formatText,
  },
}
</script>
<style lang="scss" scoped>
.models-wrap {
  background: var(--v-white-base);
  ::v-deep .menu-cell-wrapper .action-icon {
    display: none;
  }
  .top-bar {
    margin-top: 1px;
    .v-icon--disabled {
      color: var(--v-black-lighten3) !important;
      font-size: 24px;
    }
    .text--refresh {
      margin-right: 10px;
    }
  }
  .hux-data-table {
    margin-top: 1px;
    table {
      tr {
        td {
          font-size: 14px;
          height: 63px;
        }
      }
    }
  }
  ::v-deep .menu-cell-wrapper :hover .action-icon {
    display: initial;
  }
  .icon-border {
    cursor: default !important;
  }
}

.backGround-header-dropdown {
  background-color: var(--v-primary-lighten2) !important;
}
::v-deep .hux-dropdown {
  .v-btn__content {
    color: var(--v-darkBlue-base) !important;
  }
}
.col-overflow {
  white-space: nowrap !important;
  overflow: hidden !important;
  text-overflow: ellipsis !important;
}

::v-deep
  .theme--light.v-data-table
  > .v-data-table__wrapper
  > table
  > tbody
  > tr:hover:not(.v-data-table__expanded__content):not(.v-data-table__empty-wrapper) {
  background: var(--v-white-base) !important;
}
::v-deep
  .theme--light.v-data-table
  > .v-data-table__wrapper
  > table
  > thead
  > tr:last-child
  > th {
  padding-left: 32px !important;
}
::v-deep
  .theme--light.v-data-table
  > .v-data-table__wrapper
  > table
  > tbody
  > tr:not(:last-child)
  > td:not(.v-data-table__mobile-row),
.theme--light.v-data-table
  > .v-data-table__wrapper
  > table
  > tbody
  > tr:not(:last-child)
  > th:not(.v-data-table__mobile-row) {
  padding-left: 32px !important;
}
::v-deep .v-data-table > .v-data-table__wrapper > table > tbody > tr > td,
.v-data-table > .v-data-table__wrapper > table > thead > tr > td,
.v-data-table > .v-data-table__wrapper > table > tfoot > tr > td {
  padding-left: 32px !important;
}
.hr-divider {
  margin-top: -27px !important;
}
.background-empty {
  height: 70vh !important;
  background-image: url("../../assets/images/no-alert-frame.png");
  background-position: center;
}
</style>
