<template>
  <div class="team-members-wrapper">
    <v-row>
      <v-col>
        <v-card class="rounded-lg box-shadow-5 mt-3">
          <v-progress-linear
            :active="loadingAllUsers"
            :indeterminate="loadingAllUsers"
          />
          <div v-if="isDataExist" class="px-6 py-5">
            <div class="pb-1 d-flex justify-space-between">
              <div class="black--text text-h3">Team Members</div>
              <v-btn
                text
                min-width="80"
                :disabled="getRole != 'admin'"
                class="
                  d-flex
                  align-right
                  primary--text
                  text-decoration-none
                  pl-0
                  pr-0
                  idr-link
                  text-body-1
                  mt-n2
                  mr-1
                "
                data-e2e="teamMemberRequest"
                @click="toggleTeamMemberRequestDrawer()"
              >
                <icon
                  type="request-team-member"
                  :size="16"
                  :color="getRole == 'admin' ? 'primary' : 'black'"
                  :variant="getRole == 'admin' ? 'base' : 'lighten3'"
                  class="mr-3"
                />
                <span class="body-1">Request a team member</span>
              </v-btn>
            </div>
            <hux-data-table
              :columns="columnDefs"
              :sort-column="'display_name'"
              :data-items="getAllTeamMembers"
              data-e2e="team-members-table"
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
                    <avatar
                      :name="item['display_name']"
                      class="text-center"
                      :requested="
                        getRequestedMembers.findIndex(
                          (x) => x.email == item['email']
                        ) != -1
                      "
                    />
                  </template>

                  <template v-else-if="col.value === 'display_name'">
                    <span
                      class="ellipsis mt-1 d-inline"
                      :class="
                        getRequestedMembers.findIndex(
                          (x) => x.email == item['email']
                        ) != -1
                          ? 'requested'
                          : ''
                      "
                    >
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
                    <v-chip
                      v-if="
                        getRequestedMembers.findIndex(
                          (x) => x.email == item['email']
                        ) != -1
                      "
                      small
                      class="ml-1 mr-2 my-2 text-subtitle-2 requested-tag pl-2"
                      text-color="white"
                      color="grey"
                    >
                      Requested
                    </v-chip>
                  </template>

                  <template v-else-if="col.value === 'pii_access'">
                    <hux-switch
                      v-model="item[col.value]"
                      :is-disabled="
                        item['email'] == getCurrentUserEmail ||
                        getRole != 'admin' ||
                        getRequestedMembers.findIndex(
                          (x) => x.email == item['email']
                        ) != -1
                      "
                      false-color="var(--v-black-lighten4)"
                      :width="item[col.value] ? '57px' : '60px'"
                      :switch-labels="switchLabel"
                      @input="toggleAccess($event, item)"
                    />
                  </template>

                  <template v-else>
                    <span
                      :class="
                        getRequestedMembers.findIndex(
                          (x) => x.email == item['email']
                        ) != -1
                          ? 'requested'
                          : ''
                      "
                    >
                      {{ consistentNaming(item[col.value]) }}
                    </span>
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
    <team-member-request-drawer
      :toggle="teamMemberDrawer"
      class="z-index-high"
      @onToggle="(val) => (teamMemberDrawer = val)"
      @onAdd="toggleTeamMemberRequestDrawer()"
    />
  </div>
</template>

<script>
import HuxDataTable from "@/components/common/dataTable/HuxDataTable.vue"
import Avatar from "@/components/common/Avatar.vue"
import EmptyPage from "@/components/common/EmptyPage"
import HuxSwitch from "@/components/common/Switch.vue"
import { mapActions, mapGetters } from "vuex"
import Icon from "@/components/common/Icon.vue"
import TeamMemberRequestDrawer from "./TeamMemberRequestDrawer.vue"

export default {
  name: "TeamMembers",
  components: {
    EmptyPage,
    HuxDataTable,
    Avatar,
    HuxSwitch,
    Icon,
    TeamMemberRequestDrawer,
  },
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
      teamMemberDrawer: false,
      loadingAllUsers: false,
    }
  },
  computed: {
    ...mapGetters({
      getTeamMembers: "users/getUsers",
      getRequestedMembers: "users/getRequestedUsers",
      getCurrentUserEmail: "users/getEmailAddress",
      getRole: "users/getCurrentUserRole",
    }),
    isDataExist() {
      return this.getTeamMembers.length > 0
    },
    getAllTeamMembers() {
      return this.getRequestedMembers
        ? [...this.getRequestedMembers, ...this.getTeamMembers]
        : this.getTeamMembers
    },
  },
  async mounted() {
    this.loadingAllUsers = true
    try {
      await this.existingUsers()
      await this.requestUsers()
    } finally {
      this.loadingAllUsers = false
    }
  },
  methods: {
    ...mapActions({
      updateUser: "users/updatePIIAccess",
      existingUsers: "users/getUsers",
      requestUsers: "users/getRequestedUsers",
    }),
    toggleTeamMemberRequestDrawer() {
      this.teamMemberDrawer = !this.teamMemberDrawer
    },
    consistentNaming(word) {
      let replace_word = ""
      switch (word) {
        case "admin":
          replace_word = "Admin"
          break

        case "viewer":
          replace_word = "View-only"
          break

        case "editor":
          replace_word = "Edit"
          break

        default:
          replace_word = word
      }
      return replace_word
    },
    toggleAccess(value, userDetails) {
      this.updateUser({
        id: userDetails.id,
        pii_access: value,
      })
    },
  },
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
          height: 32px !important;
          box-shadow: none !important;
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
.z-index-high {
  z-index: 100;
}
.requested {
  font-style: italic;
  font-weight: normal;
  font-size: 16px;
  line-height: 22px;
  color: var(--v-black-lighten3);
}
.requested-tag {
  height: 20px;
  width: 80px;
}
</style>
