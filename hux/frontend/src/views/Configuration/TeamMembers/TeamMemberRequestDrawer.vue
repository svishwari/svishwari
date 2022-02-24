<template>
  <drawer v-model="localToggle" :width="600" :loading="loading">
    <template #header-left>
      <div class="d-flex align-center">
        <icon type="team-member-drawer" :size="32" class="mr-3" />
        <h3 class="text-h2">Request a team member to add</h3>
      </div>
    </template>

    <template #default>
      <div class="pa-6">
        <span class="body-1"
          >Provide the information about the new team member.
        </span>
        <v-row>
          <v-col class="py-0 mt-7">
            <span class="body-2 adjust-label">First name</span>
            <text-field
              v-model="firstName"
              placeholder-text="Enter first name"
              data-e2e="firstName"
              required
            ></text-field>
          </v-col>
        </v-row>
        <v-row>
          <v-col class="py-0">
            <span class="body-2 adjust-label">Last name</span>
            <text-field
              v-model="lastName"
              placeholder-text="Enter last name"
              data-e2e="lastName"
              required
            ></text-field>
          </v-col>
        </v-row>
        <v-row>
          <v-col class="py-0">
            <span class="body-2 adjust-label">Email</span>
            <text-field
              v-model="email"
              placeholder-text="example@example.com"
              data-e2e="email"
              required
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
              min-width="340"
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
                    <span v-html="pii.hoverTooltip" />
                  </template>
                </tooltip>
              </span>
              <hux-switch
                v-model="togglePii"
                false-color="var(--v-black-lighten4)"
                :width="togglePii ? '57px' : '60px'"
                :switch-labels="switchLabel"
                data-e2e="togglePii"
              />
            </div>
          </v-col>
        </v-row>
        <v-row>
          <v-col class="py-0 mt-7">
            <span class="body-2 adjust-label">Reason for request</span>
            <v-textarea
              v-model="requestText"
              solo
              flat
              hide-details
              no-resize
              rows="4"
              class="body-2 mt-1 border-fix"
              placeholder="Please elaborate on your request"
              data-e2e="requestText"
            />
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
          @click="requestTeamMember()"
        >
          Request
        </hux-button>
      </div>
    </template>
  </drawer>
</template>

<script>
import { mapGetters, mapActions } from "vuex"
import Drawer from "@/components/common/Drawer.vue"
import HuxButton from "@/components/common/huxButton.vue"
import Tooltip from "@/components/common/Tooltip.vue"
import Icon from "@/components/common/Icon.vue"
import TextField from "@/components/common/TextField.vue"
import HuxDropdown from "@/components/common/HuxDropdown.vue"
import HuxSwitch from "@/components/common/Switch.vue"

export default {
  name: "AudiencesDrawer",

  components: {
    Drawer,
    HuxButton,
    Tooltip,
    Icon,
    TextField,
    HuxDropdown,
    HuxSwitch,
  },

  props: {
    toggle: {
      type: Boolean,
      required: false,
      default: false,
    },
  },

  data() {
    return {
      localToggle: false,
      loading: false,
      accessLevel: "Select access",
      accessLevelType: "",
      listOfLevels: [
        {
          name: "Admin",
          type: "admin",
        },
        {
          name: "View-only",
          type: "viewer",
        },
        {
          name: "Edit",
          type: "editor",
        },
      ],
      firstName: "",
      lastName: "",
      email: "",
      togglePii: false,
      requestText: "",
      pii: {
        hoverTooltip:
          "Sensitive and PII data are only accessible to individuals tha been granted permission by an Admin.",
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
      return !(
        this.firstName &&
        this.lastName &&
        this.email &&
        this.accessLevelType &&
        this.requestText
      )
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

  methods: {
    ...mapActions({
      reqTeamMember: "users/requestTeamMember",
      getreqMembers: "users/getRequestedUsers",
    }),
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
    reset() {
      this.firstName = ""
      this.lastName = ""
      this.email = ""
      this.togglePii = false
      this.requestText = ""
      this.accessLevel = "Select access"
      this.accessLevelType = ""
    },
    async requestTeamMember() {
      this.loading = true
      const payload = {
        first_name: this.firstName,
        last_name: this.lastName,
        email: this.email,
        access_level: this.accessLevelType,
        pii_access: this.togglePii,
        reason_for_request: this.requestText,
      }
      this.reset()
      this.closeDrawer()
      try {
        await this.reqTeamMember(payload)
        await this.getreqMembers()
      } finally {
        this.loading = false
      }
    },
  },
}
</script>

<style lang="scss" scoped>
::v-deep .hux-dropdown {
  .main-button {
    border-radius: 4px;
    .v-btn__content {
      top: 1px;
      .v-icon {
        top: -1px;
      }
    }
  }
}
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
</style>
