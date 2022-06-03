<template>
  <drawer v-model="localToggle" :width="600" :loading="loading">
    <template #header-left>
      <div class="d-flex align-center pl-2">
        <icon type="team-member-drawer" :size="32" class="mr-3" />
        <h3 class="text-h2">Edit {{ data.display_name }}</h3>
      </div>
    </template>

    <template #default>
      <div class="pa-6">
        <span class="body-1">Edit information about the team member. </span>
        <v-row>
          <v-col class="py-0 mt-7">
            <span class="body-2 adjust-label">First name</span>
            <text-field
              v-model="data.display_name.split(' ')[0]"
              placeholder-text="Edit first name"
              data-e2e="firstName"
              required
              :disabled="true"
            ></text-field>
          </v-col>
        </v-row>
        <v-row>
          <v-col class="py-0">
            <span class="body-2 adjust-label">Last name</span>
            <text-field
              v-model="data.display_name.split(' ')[1]"
              placeholder-text="Edit last name"
              data-e2e="lastName"
              required
              :disabled="true"
            ></text-field>
          </v-col>
        </v-row>
        <v-row>
          <v-col class="py-0">
            <span class="body-2 adjust-label">Email</span>
            <text-field
              v-model="data.email"
              placeholder-text="example@example.com"
              data-e2e="email"
              required
              :disabled="true"
            ></text-field>
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="7" class="py-0 adjust-access">
            <span class="body-2 adjust-label">
              <tooltip max-width="200px" position-top>
                <template #label-content>
                  <span class="body-2 adjust-label">Access level</span>
                  <icon
                    type="info"
                    :size="8"
                    class="ml-1 mb-1"
                    color="primary"
                    variant="base"
                  />
                </template>
                <template #hover-content>
                  <div class="body-2 pd-6">
                    <div class="font-weight-bold mb-3">Admin access</div>
                    <div class="mb-6">
                      Ability to select who has access to view PII data and have
                      removal/add functionality across Hux.
                    </div>
                    <div class="font-weight-bold mb-3">Edit access</div>
                    <div class="mb-6">
                      Have removal/add functionality across Hux.
                    </div>
                    <div class="font-weight-bold mb-3">View-only access</div>
                    <div>
                      Unable to edit a client’s team, or remove and add any
                      solutions across Hux.
                    </div>
                  </div>
                </template>
              </tooltip>
            </span>
            <hux-dropdown
              :label="accessLevel"
              :selected="accessLevel"
              :items="listOfLevels"
              min-width="341"
              data-e2e="accessLevel"
              @on-select="onSelectMenuItem"
            />
          </v-col>
          <v-col cols="5" class="py-0">
            <div class="d-flex align-items-center pii-box">
              <span class="body-2 adjust-pii mr-1">
                <tooltip :max-width="pii.tooltipWidth" position-top>
                  <template #label-content>
                    <span class="body-2">PII access</span>
                    <icon
                      type="info"
                      :size="8"
                      class="ml-1 mb-1"
                      color="primary"
                      variant="base"
                    />
                  </template>
                  <template #hover-content>
                    <span v-bind.prop="formatInnerHTML(pii.hoverTooltip)" />
                  </template>
                </tooltip>
              </span>
              <hux-switch
                v-model="pii_access"
                false-color="var(--v-black-lighten4)"
                :width="pii_access ? '57px' : '60px'"
                :switch-labels="switchLabel"
                data-e2e="togglePii"
              />
            </div>
          </v-col>
        </v-row>
        <v-row>
          <v-col class="pa-0 del-text">
            <v-btn class="remove-button px-0" @click="$emit('onDelete')">
              <hux-icon
                type="delete-button"
                :size="18"
                color="error"
                class="mr-4"
              />
              <span class="text-body-1 error--text">
                Remove this user from this team
              </span>
            </v-btn>
          </v-col>
        </v-row>
      </div>
    </template>

    <template #footer-left>
      <hux-button
        variant="white"
        size="large"
        :is-tile="true"
        class="mr-2 btn-border box-shadow-none"
        @click="closeDrawer"
      >
        <span class="primary--text">Cancel</span>
      </hux-button>
    </template>
    <template #footer-right>
      <div class="d-flex align-baseline">
        <hux-button
          variant="primary"
          size="large"
          :is-tile="true"
          :is-disabled="formFilled"
          data-e2e="request"
          @click="editTeamMember()"
        >
          Request
        </hux-button>
      </div>
    </template>
  </drawer>
</template>

<script>
import { mapGetters, mapActions } from "vuex"
import { formatInnerHTML } from "@/utils"
import Drawer from "@/components/common/Drawer.vue"
import HuxButton from "@/components/common/huxButton.vue"
import Tooltip from "@/components/common/Tooltip.vue"
import Icon from "@/components/common/Icon.vue"
import TextField from "@/components/common/TextField.vue"
import HuxDropdown from "@/components/common/HuxDropdown.vue"
import HuxSwitch from "@/components/common/Switch.vue"
import HuxIcon from "@/components/common/Icon.vue"

export default {
  name: "EditTeamMemberDrawer",

  components: {
    Drawer,
    HuxButton,
    Tooltip,
    Icon,
    TextField,
    HuxDropdown,
    HuxSwitch,
    HuxIcon,
  },

  props: {
    toggle: {
      type: Boolean,
      required: false,
      default: false,
    },
    data: {
      type: Object,
      require: true,
      default: () => {},
    },
  },

  data() {
    return {
      localToggle: false,
      loading: false,
      listOfLevels: [
        {
          name: "Admin",
          type: "admin",
        },
        {
          name: "Edit",
          type: "editor",
        },
        {
          name: "View-only",
          type: "viewer",
        },
      ],
      accessLevel: "Select Access",
      accessLevelType: "",
      pii_access: false,
      pii: {
        hoverTooltip:
          "Sensitive and PII data are only accessible to individuals that have been granted permission by an Admin.",
        tooltipWidth: "300px",
      },
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
    ...mapGetters({}),
    formFilled() {
      return (
        this.accessLevelType == this.data.role &&
        this.pii_access == this.data.pii_access
      )
    },
    setAccessLevel() {
      return this.listOfLevels.find((item) => item.type == this.data.role)
    },
  },

  watch: {
    toggle(value) {
      this.localToggle = value
    },

    localToggle(value) {
      this.$emit("onToggle", value)
    },
  },

  updated() {
    this.accessLevel = this.setAccessLevel.name
    this.accessLevelType = this.setAccessLevel.type
    this.pii_access = this.data.pii_access
  },

  methods: {
    ...mapActions({
      updateUser: "users/updateUser",
      reqTeamMember: "users/requestTeamMember",
      getreqMembers: "users/getRequestedUsers",
      existingUsers: "users/getUsers",
    }),
    formatInnerHTML: formatInnerHTML,
    closeDrawer() {
      this.localToggle = false
    },
    onSelectMenuItem(item) {
      if (this.accessLevel == item.name) {
        this.accessLevel = "Select access"
        this.accessLevelType = ""
      } else {
        this.accessLevel = item.name
        this.accessLevelType = item.type
      }
    },
    async editTeamMember() {
      await this.updateUser({
        id: this.data.id,
        pii_access: this.pii_access,
        role: this.accessLevelType,
      })
      this.closeDrawer()
      this.existingUsers()
    },
  },
}
</script>

<style lang="scss" scoped>
.adjust-label {
  position: relative;
  bottom: -4px !important;
  margin-left: 6px !important;
}
.adjust-access {
  position: relative;
  left: -8px !important;
  top: -5px !important;
}
.adjust-pii {
  position: relative;
  left: -8px !important;
  top: 22px !important;
}
.pii-box {
  position: relative;
  top: 14px !important;
  left: 70px;
  width: 150px !important;
}
.border-fix {
  border: 1px solid #d0d0ce;
}
.del-text {
  display: flex;
  margin-top: 68px;
  margin-left: 12px;
  align-items: center;
}
.remove-button {
  background-color: inherit !important;
  box-shadow: none;
  &:hover {
    background-color: inherit !important;
  }
}

::v-deep .text-field-hux.v-input.v-input__slot {
  background-color: var(v-primary-lighten1) !important;
}
</style>
