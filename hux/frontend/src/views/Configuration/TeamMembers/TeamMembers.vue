<template>
  <div class="team-members-wrapper">
    <v-row>
      <v-col>
        <v-card class="rounded-lg box-shadow-5">
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
                  :class="col.value === '' ? 'text-center' : 'text-left'"
                  :style="{ width: col.width }"
                >
                  <template v-if="col.value === ''">
                    <avatar :name="item['display_name']" class="text-center" />
                  </template>

                  <template v-else-if="col.value === 'display_name'">
                    <span class="ellipsis mt-1 d-inline">
                      {{ item[col.value] }}
                    </span>
                    <v-chip
                      v-if="item['email'] == getCurrentUserEmail"
                      small
                      class="mr-2 my-2 text-subtitle-2 you-tag pl-2"
                      text-color="white"
                      color="yellow"
                    >
                      You
                    </v-chip>
                  </template>

                  <template v-else-if="col.value === 'pii_access'">
                    <hux-switch
                      v-model="item[col.value]"
                      :is-disabled="
                        item['email'] == getCurrentUserEmail ||
                        getRole != 'admin'
                      "
                      false-color="var(--v-black-lighten4)"
                      :width="item[col.value] ? '57px' : '60px'"
                      :switch-labels="switchLabel"
                    />
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
import EmptyPage from "@/components/common/EmptyPage"
import HuxSwitch from "@/components/common/Switch.vue"
import { mapGetters } from "vuex"

export default {
  name: "TeamMembers",
  components: { EmptyPage, HuxDataTable, Avatar, HuxSwitch },
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
          hoverTooltip:
            "Admin access <br /><br />\
            Ability to select who has access to view PII data and have removal/add functionality across Hux.<br /><br />\
            Edit access <br /><br />\
            Have removal/add functionality across Hux.<br /><br />\
            View-only access <br /><br />\
            Unable to edit a client’s team, or remove and add any solutions across Hux.",
          tooltipWidth: "200px",
        },
        {
          text: "PII Access",
          value: "pii_access",
          width: "97px",
          hoverTooltip:
            "Sensitive and PII data are only accessible to individuals tha been granted permission by an Admin.",
          tooltipWidth: "300px",
        },
      ],
      switchLabel: [
        {
          condition: true,
          label: "ON",
        },
        {
          condition: false,
          label: "OFF",
        },
      ],
    }
  },
  computed: {
    ...mapGetters({
      getTeamMembers: "users/getUsers",
      getCurrentUserEmail: "users/getEmailAddress",
      getRole: "users/getCurrentUserRole",
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
.you-tag {
  height: 20px;
  width: 39px;
}
</style>
