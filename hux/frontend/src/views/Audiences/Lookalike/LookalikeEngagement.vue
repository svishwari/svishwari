<template>
  <v-card class="rounded-lg card-style delivery-overview mt-4" flat>
    <v-card-title class="d-flex justify-space-between pb-0 pl-6 pt-5">
      <div class="text-h3 mb-2">Engagements</div>
    </v-card-title>
    <!-- <v-progress-linear
      v-if="loadingRelationships"
      :active="loadingRelationships"
      :indeterminate="loadingRelationships"
    /> -->

    <v-list dense class="pb-0 pl-6 pt-3 delivery-table">
      <hux-data-table
        :columns="headers"
        :sort-desc="true"
        :data-items="sections"
      >
        <template #row-item="{ item }">
          <td
            v-for="header in headers"
            :key="header.value"
            class="text-body-2 column"
            :style="{ width: header.width }"
          >
            <div v-if="header.value == 'name'" class="text-body-1 d-flex h-25">
              <router-link
                :to="{
                  name: 'AudienceInsight',
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
              <!-- <time-stamp
                :value="
                  tableData != ''
                    ? item[tableData]['update_time']
                    : sections['update_time']
                "
              /> -->
              -
            </div>
          </td>
        </template>
      </hux-data-table>
      <v-list dense class="add-list audience-block" :height="60">
        <v-list-item @click="$emit('triggerSelectAudience', $event)">
          <tooltip>
            <template #label-content>
              <hux-icon
                type="plus"
                :size="15"
                color="primary"
                class="mr-1 mb-2"
              />
              <hux-icon
                type="engagement_circle"
                :size="31"
                color="primary"
                class="mr-1"
              />
            </template>
            <template #hover-content>
              <div class="py-2 white d-flex flex-column">
                <span> Add a audience to this engagement </span>
              </div>
            </template>
          </tooltip>
          <span
            min-width="7rem"
            height="2rem"
            class="primary--text text-body-1 mb-1"
          >
            Engagement
          </span>
        </v-list-item>
      </v-list>
    </v-list>

    <!-- <v-card-text class="pl-6 pr-6 pb-6 pt-0">
      <div class="empty-state py-2 black--text text--lighten-4 text-body-1">
        <span>
          This lookalike is not part of any engagements. Add it to an engagement below.
        </span>
      </div>

      <v-list dense class="add-list" :height="52">
        <v-list-item @click="$emit('addEngagement')" class="empty-engagement">
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
            class="primary--text text-body-1"
          >
            <span class="destination_text">Engagement</span>
          </v-btn>
        </v-list-item>
      </v-list>
    </v-card-text> -->
  </v-card>
</template>
<script>
// import Logo from "./Logo.vue"
import HuxDataTable from "@/components/common/dataTable/HuxDataTable.vue"
import Icon from "@/components/common/Icon.vue"
import HuxIcon from "@/components/common/Icon.vue"
import Tooltip from "@/components/common/Tooltip.vue"
import Status from "@/components/common/Status.vue"

export default {
  name: "LookalikeEngagement",
  components: {
    Icon,
    Tooltip,
    HuxIcon,
    HuxDataTable,
    Status,
  },
  props: {
    sections: {
      type: Object,
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
  ::v-deep .v-data-table__wrapper {
    tbody {
      tr {
        td:nth-child(1) {
          &:hover,
          &:focus {
            .action-icon {
              display: block !important;
            }
          }
        }
      }
    }
  }
}
</style>