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
                :ripple="false"
                :disabled="getRole != 'admin'"
                class="
                  d-flex
                  align-right
                  primary--text
                  text-decoration-none
                  pl-0
                  pr-0
                  team-member-request-button
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
                    <span class="menu-wrap" data-e2e="member-list">
                      <span>
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
                          class="
                            ml-1
                            mr-2
                            my-2
                            text-subtitle-2
                            requested-tag
                            pl-2
                          "
                          text-color="white"
                          color="grey"
                        >
                          Requested
                        </v-chip>
                      </span>

                      <v-spacer> </v-spacer>
                      <span
                        class="
                          action-icon
                          font-weight-light
                          float-right
                          d-none
                          menu-activator
                        "
                      >
                        <v-menu
                          v-model="openMenu[item.id]"
                          class="menu-wrapper"
                          bottom
                          offset-y
                        >
                          <template #activator="{ on, attrs }">
                            <v-icon
                              v-bind="attrs"
                              class="mr-2 more-action"
                              color="primary"
                              data-e2e="member-list-dots"
                              v-on="on"
                              @click.prevent
                            >
                              mdi-dots-vertical
                            </v-icon>
                          </template>
                          <v-list class="menu-list-wrapper">
                            <v-list-item-group>
                              <v-list-item
                                v-for="option in options.filter(
                                  (x) => !x.isHidden
                                )"
                                :key="option.id"
                                :disabled="!option.active"
                                @click="option['onClick'](item)"
                              >
                                <v-list-item-title v-if="!option.menu">
                                  {{ option.title }}
                                </v-list-item-title>
                              </v-list-item>
                            </v-list-item-group>
                          </v-list>
                        </v-menu>
                      </span>
                    </span>
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
    <edit-team-member-drawer
      :toggle="editTeamMember"
      :data="editTeamMemberObj"
      class="z-index-high"
      @onToggle="(val) => (editTeamMember = val)"
      @onDelete="
        deleteTeamMemberObj = editTeamMemberObj
        deleteTeamMember = true
      "
      @onEdit="toggleEditTeamMemberDrawer()"
    />
    <confirm-modal
      v-model="deleteTeamMember"
      icon="sad-face"
      type="error"
      title="You are about to remove"
      :sub-title="`${
        deleteTeamMemberObj.display_name
          ? deleteTeamMemberObj.display_name.split(' ')[0]
          : ''
      } from ${
        demoConfiguration.demo_mode ? demoConfiguration.industry : 'Retail'
      } Client`"
      right-btn-text="Yes, remove user"
      data-e2e="remove-team-member-confirmation"
      body="Are you sure you want to remove this person? Removing this person from this team will require you to request them again so that they can regain access to this client."
      @onCancel="deleteTeamMember = !deleteTeamMember"
      @onConfirm="deleteTeamMemberFunc(deleteTeamMemberObj.id)"
    >
    </confirm-modal>
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
import EditTeamMemberDrawer from "./EditTeamMemberDrawer.vue"
import ConfirmModal from "@/components/common/ConfirmModal.vue"
import { getAccess } from "@/utils"

export default {
  name: "TeamMembers",
  components: {
    EmptyPage,
    HuxDataTable,
    Avatar,
    HuxSwitch,
    Icon,
    TeamMemberRequestDrawer,
    EditTeamMemberDrawer,
    ConfirmModal,
  },
  data() {
    return {
      columnDefs: [
        {
          text: "",
          value: "",
          width: "76px",
          sortable: false,
        },
        {
          text: "Name",
          value: "display_name",
          width: "281px",
          sortable: true,
        },
        {
          text: "Email",
          value: "email",
          width: "367px",
          sortable: true,
        },
        {
          text: "Access Level",
          value: "access_level",
          width: "163px",
          hoverTooltip:
            "<b>Admin access</b> <br /><br />\
            Ability to select who has access to view PII data and have removal/add functionality across Hux.<br /><br />\
            <b>Edit access</b> <br /><br />\
            Have removal/add functionality across Hux.<br /><br />\
            <b>View-only access</b> <br /><br />\
            Unable to edit a client’s team, or remove and add any solutions across Hux.",
          tooltipWidth: "200px",
          sortable: true,
        },
        {
          text: "PII Access",
          value: "pii_access",
          width: "97px",
          hoverTooltip:
            "Sensitive and PII data are only accessible to individuals tha been granted permission by an Admin.",
          tooltipWidth: "300px",
          sortable: true,
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
      editTeamMember: false,
      editTeamMemberObj: {
        role: "",
        id: "",
        pii_access: false,
        display_name: "",
        access_level: "",
        email: "",
      },
      loadingAllUsers: false,
      deleteTeamMember: false,
      deleteTeamMemberObj: {},
      options: [
        {
          title: "Edit",
          active: true,
          onClick: (item) => {
            this.editTeamMember = true
            this.editTeamMemberObj = item
          },
          isHidden: !this.getAccess("user", "update_one"),
        },
        {
          title: "Remove",
          active: true,
          onClick: (item) => {
            this.deleteTeamMember = true
            this.deleteTeamMemberObj = item
          },
        },
      ],
      openMenu: {},
    }
  },
  computed: {
    ...mapGetters({
      getTeamMembers: "users/getUsers",
      getRequestedMembers: "users/getRequestedUsers",
      getCurrentUserEmail: "users/getEmailAddress",
      getRole: "users/getCurrentUserRole",
      demoConfiguration: "users/getDemoConfiguration",
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

  watch: {
    // To reset the value of the openMenu
    openMenu(newValue) {
      if (!newValue) this.openMenu = {}
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
      updateUser: "users/updateUser",
      existingUsers: "users/getUsers",
      requestUsers: "users/getRequestedUsers",
      deleteUsers: "users/deleteUser",
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
    async deleteTeamMemberFunc(id) {
      await this.deleteUsers(id)
      this.deleteTeamMember = !this.deleteTeamMember
      this.existingUsers()
    },
    getAccess: getAccess,
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
          z-index: 0;
        }
      }
    }
    tr {
      td {
        height: 60px !important;
      }
      td:nth-child(2) {
        &:hover,
        &:focus {
          .action-icon {
            display: block !important;
          }
        }
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
.team-member-request-button {
  &::before {
    background-color: transparent;
  }
}
.menu-wrap {
  display: flex;
  align-items: center;
}
.v-menu__content .v-list-item.theme--light {
  min-height: 32px !important;
}
</style>
