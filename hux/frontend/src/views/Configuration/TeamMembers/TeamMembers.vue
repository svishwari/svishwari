<template>
  <div class="team-members-wrapper">
    <v-row>
      <v-col>
        <v-card
          class="rounded-lg box-shadow-5"
          :height="isDataExist ? 641 : 280"
        >
          <div v-if="isDataExist" class="pa-5">
            <div class="pb-4 black--text text-h3">Team Members</div>
            <hux-data-table
              :columns="columnDefs"
              :sort-column="'display_name'"
              :data-items="getTeamMembers"
            >
              <template #row-item="{ item }">
                <td
                  v-for="col in columnDefs"
                  :key="col.value"
                  class="black--text text-body-1"
                  :style="{ width: col.width }"
                >
                  <template v-if="col.value === ''">
                    <avatar :name="item['display_name']" />
                  </template>

                  <template v-else-if="col.value === 'display_name'">
                    <tooltip>
                      <template slot="label-content">
                        <span class="ellipsis mt-1">
                          {{ item[col.value] }}
                        </span>
                      </template>
                      <template slot="hover-content">
                        {{ item[col.value] }}
                      </template>
                    </tooltip>
                  </template>

                  <template v-else>
                    {{ item[col.value] }}
                  </template>
                </td>
              </template>
            </hux-data-table>
          </div>
          <v-row v-else class="team-members-table-frame py-14">
            <empty-page type="user" :size="50">
              <template #title>
                <div class="title-no-notification">No team members</div>
              </template>
              <template #subtitle>
                <div class="des-no-notification">
                  The list of team mebers will appear here once the invitation
                  has been accepted. Please check back later.
                </div>
              </template>
            </empty-page>
          </v-row>
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>

<script>
import HuxDataTable from "@/components/common/dataTable/HuxDataTable.vue"
import Avatar from "@/components/common/Avatar.vue"
import Tooltip from "@/components/common/Tooltip.vue"
import EmptyPage from "@/components/common/EmptyPage"
import { mapGetters } from "vuex"

export default {
  name: "TeamMembers",
  components: { EmptyPage, HuxDataTable, Avatar, Tooltip },
  data() {
    return {
      columnDefs: [
        {
          text: "",
          value: "",
          width: "76px",
        },
        {
          text: "Name",
          value: "display_name",
          width: "281px",
        },
        {
          text: "Email",
          value: "email",
          width: "367px",
        },
        {
          text: "Access Level",
          value: "access_level",
          width: "163px",
        },
        {
          text: "PII Access",
          value: "pii_access",
          width: "97px",
        },
      ],
    }
  },
  computed: {
    ...mapGetters({
      getTeamMembers: "users/getUsers",
    }),
    isDataExist() {
      return this.getTeamMembers.length > 0
    },
  },
  methods: {},
}
</script>

<style lang="scss" scoped>
.team-members-wrapper {
  .team-members-table-frame {
    background-image: url("../../../assets/images/no-lift-chart-frame.png");
    background-position: center;
  }
}
.hux-data-table {
  ::v-deep table {
    .v-data-table-header {
      tr {
        th {
          background: var(--v-primary-lighten2);
          height: 40px !important;
        }
      }
    }
    tr {
      td {
        height: 60px !important;
      }
    }
    .ellipsis {
      overflow: hidden;
      text-overflow: ellipsis;
      max-width: 28ch;
      display: inline-block;
      width: 28ch;
      white-space: nowrap;
    }
    border-radius: 12px 12px 0px 0px;
    overflow: hidden;
  }
}
</style>
