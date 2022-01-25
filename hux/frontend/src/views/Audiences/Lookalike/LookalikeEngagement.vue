<template>
  <v-card class="rounded-lg card-style delivery-overview mt-6" flat>
    <v-card-title class="d-flex justify-space-between pb-0 pl-6 pt-5">
      <div class="text-h3 mb-2">Engagements</div>
    </v-card-title>
    <v-card-text class="pl-6 pr-6 pb-6 pt-3">
      <div v-if="sections && sections.length > 0">
        <hux-data-table
          class="delivery-table"
          :columns="headers"
          :sort-desc="true"
          :data-items="sections"
        >
          <template #row-item="{ item }">
            <td
              v-for="header in headers"
              :key="header.value"
              class="text-body-2"
              :style="{ width: header.width }"
            >
              <div
                v-if="header.value == 'name'"
                class="text-body-1 d-flex h-25"
              >
                <router-link
                  :to="{
                    name: 'EngagementDashboard',
                    params: { id: item.id },
                  }"
                  class="text-decoration-none"
                  append
                >
                  <span class="ellipsis primary--text">
                    {{ item.name }}
                  </span>
                </router-link>
              </div>
              <div v-if="header.value == 'status'" class="text-body-1">
                <status
                  :status="item['status']"
                  :show-label="true"
                  class="d-flex"
                  :icon-size="17"
                />
              </div>
              <div v-if="header.value == 'created'" class="text-body-1">
                <time-stamp :value="item['create_time']" />
              </div>
            </td>
          </template>
        </hux-data-table>

        <v-list dense class="add-list list-border" :height="52">
          <v-list-item @click="$emit('addEngagement')">
            <tooltip>
              <template #label-content>
                <hux-icon
                  type="plus"
                  :size="16"
                  color="primary"
                  class="mr-2 plus-icon"
                />
                <hux-icon
                  type="engagement_circle"
                  :size="34"
                  color="primary"
                  class="mr-0 mb-n1"
                />
              </template>
              <template #hover-content>
                <div class="py-2 white d-flex flex-column">
                  <span> Add a destination to this engagement </span>
                </div>
              </template>
            </tooltip>
            <v-btn
              text
              min-width="7rem"
              height="2rem"
              class="primary--text text-body-1 mt-n1"
            >
              <span class="destination_text">Engagement</span>
            </v-btn>
          </v-list-item>
        </v-list>
      </div>

      <div v-else class="empty-state black--text text--lighten-4 text-body-1">
        <div class="mb-1">
          This lookalike is not part of any engagements. Add it to an engagement
          below.
        </div>
        <v-list dense class="add-list" :height="52">
          <v-list-item class="px-0" @click="$emit('addEngagement')">
            <hux-icon type="plus" :size="16" color="primary" class="mr-2" />
            <hux-icon
              type="engagement_circle"
              :size="34"
              color="primary"
              class="mr-0 mb-n1"
            />
            <v-btn
              text
              min-width="7rem"
              height="2rem"
              class="primary--text text-body-1"
            >
              <span class="destination_text">Engagement</span>
            </v-btn>
          </v-list-item>
        </v-list>
      </div>
    </v-card-text>
  </v-card>
</template>
<script>
import HuxDataTable from "@/components/common/dataTable/HuxDataTable.vue"
import HuxIcon from "@/components/common/Icon.vue"
import Tooltip from "@/components/common/Tooltip.vue"
import Status from "@/components/common/Status.vue"
import TimeStamp from "@/components/common/huxTable/TimeStamp.vue"

export default {
  name: "LookalikeEngagement",
  components: {
    Tooltip,
    HuxIcon,
    HuxDataTable,
    Status,
    TimeStamp,
  },
  props: {
    sections: {
      type: Array,
      required: true,
    },
    headers: {
      type: Array,
      required: true,
    },
  },
}
</script>
<style lang="scss" scoped>
.destination_text {
  margin-top: -2px;
}
.plus-icon {
  margin-bottom: 7px;
}
.empty-engagement {
  padding-left: 0px !important;
}
.delivery-table {
  ::v-deep .v-data-table {
    .v-data-table-header {
      tr {
        height: 32px !important;
      }
      th {
        background: var(--v-primary-lighten2);
      }
    }
  }
  ::v-deep .v-data-table .v-data-table-header th:first-child {
    border-top-left-radius: 12px !important;
  }
  ::v-deep .v-data-table .v-data-table-header th:last-child {
    border-top-right-radius: 12px !important;
  }
}
.list-border {
  border-bottom: thin solid rgba(0, 0, 0, 0.12) !important;
}
::v-deep .theme--light.v-data-table.v-data-table--fixed-header thead th {
  box-shadow: none !important;
}
</style>
