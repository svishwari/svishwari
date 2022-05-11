<template>
  <div class="brand-settings-wrapper">
    <v-row>
      <v-col>
        <v-card class="rounded-lg box-shadow-5 mt-3">
          <div class="px-6 py-5">
            <div class="pb-1 d-flex justify-space-between">
              <div class="black--text text-h3">
                Customize this client’s brand
              </div>
            </div>
            <div class="black--text text-body-1 mt-4">
              Customize this client’s look and feel based on the industry you
              select. This will update the client’s name, homepage, copy, and
              iconography.
            </div>
            <div class="black--text text-body-1">
              Note: This will only update the look and feel for you, not for all
              team members.
            </div>
            <div class="black--text text-h6 d-flex mt-4">
              <h3 class="text-body-1">Demo mode</h3>
              <tooltip position-top>
                <template #label-content>
                  <icon
                    type="info"
                    :size="10"
                    class="mb-1 ml-1"
                    color="primary"
                    variant="base"
                  />
                </template>
                <template #hover-content>
                  Switching on demo mode will change the look and feel based on
                  a selected industry. This will only apply to you. Switching
                  off demo mode will return the client’s look and feel back to
                  default.
                </template>
              </tooltip>
              <hux-switch
                v-model="showConfiguration"
                false-color="var(--v-black-lighten4)"
                width="57px"
                :switch-labels="toggleSwitchLabels"
                class="w-53"
                @change="toggleMainSwitch($event)"
              />
            </div>
            <div v-if="enableSelection" class="black--text text-h6 mt-4">
              <label class="mb-1">Industry</label>
              <hux-dropdown
                :label="newAppDetails['category']"
                :selected="newAppDetails['category']"
                :items="categoryOptions"
                min-width="240"
                @on-select="onSelectMenuItem"
              />
            </div>

            <div v-if="enableSelection" class="black--text text-h6 mt-4">
              <div v-for="label in labels" :key="label">
                <label class="mb-1">{{ label }}</label>
                <hux-dropdown
                  :label="newAppDetails['category']"
                  :selected="newAppDetails['category']"
                  :items="categoryOptions"
                  min-width="240"
                  @on-select="onSelectMenuItem"
                />
              </div>
            </div>
          </div>
        </v-card>
      </v-col>
    </v-row>
    <hux-footer slot="footer" data-e2e="footer" max-width="100%">
      <template #right>
        <hux-button
          size="large"
          height="40"
          is-tile
          variant="primary base"
          data-e2e="action-audience"
        >
          Update
        </hux-button>
      </template>
    </hux-footer>
  </div>
</template>

<script>
import { mapActions, mapGetters } from "vuex"
import Icon from "@/components/common/Icon.vue"
import Tooltip from "@/components/common/Tooltip.vue"
import HuxSwitch from "@/components/common/Switch.vue"
import HuxButton from "@/components/common/huxButton"
import HuxFooter from "@/components/common/HuxFooter"
import HuxDropdown from "@/components/common/HuxDropdown.vue"

export default {
  name: "BrandSettings",
  components: {
    HuxSwitch,
    Icon,
    Tooltip,
    HuxButton,
    HuxFooter,
    HuxDropdown,
  },
  data() {
    return {
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
      showConfiguration: false,
      toggleSwitchLabels: [
        {
          condition: true,
          label: "ON",
        },
        {
          condition: false,
          label: "OFF",
        },
      ],
      newAppDetails: {
        category: "Select",
        name: null,
        url: null,
      },
      labels: [
        "What describes best this client?",
        "Who is the client’s target audience?",
        "What does the client wish to track? ",
      ],
      categoryOptions: [],
      enableSelection: false,
      industrySelected: false,
    }
  },
  computed: {
    ...mapGetters({
      //   getTeamMembers: "users/getUsers",
      //   getRequestedMembers: "users/getRequestedUsers",
      //   getCurrentUserEmail: "users/getEmailAddress",
      //   getRole: "users/getCurrentUserRole",
    }),
  },
  async mounted() {
    // try {
    //   await this.existingUsers()
    //   await this.requestUsers()
    // } finally {
    //   this.loadingAllUsers = false
    // }
  },
  methods: {
    ...mapActions({
      //   updateUser: "users/updatePIIAccess",
      //   existingUsers: "users/getUsers",
      //   requestUsers: "users/getRequestedUsers",
    }),
    toggleMainSwitch(value) {
      this.enableSelection = value
    },
  },
}
</script>

<style lang="scss" scoped>
.brand-settings-wrapper {
  ::v-deep.v-input--selection-controls {
    margin-top: 0px !important;
    padding-top: 0px !important;
    margin-left: 21px !important;
  }
}
</style>
