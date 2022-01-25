<template>
  <drawer
    v-model="localDrawer"
    :content-padding="'pa-0'"
    :content-header-padding="'px-3'"
  >
    <template #header-left>
      <div v-if="getNotificationPreferences" class="d-flex align-center">
        <icon
          type="setting-gear-border"
          :size="32"
          color="black"
          class="d-block mr-2 black-border"
        />
        <h3 class="text-h2 ml-1 black--text text--darken-4">
          Configure alerts
        </h3>
      </div>
    </template>
    <template #default>
      <div class="px-6 py-4">
        <div class="text-body-1 pb-4">
          Configure if you wish to recieve Hux notifications and alerts via
          email.
        </div>
        <div class="d-flex full-alert text-body-1 pb-4">
          Do you wish to receive alerts?
          <hux-switch
            v-model="showAlerts"
            false-color="var(--v-black-lighten4)"
            width="57px"
            :switch-labels="switchLabelFullAlerts"
            class="w-53"
          />
        </div>
        <div v-if="showAlerts">
          <div class="pb-4 h-77">
            <tooltip position-top>
              <template #label-content>
                Email
                <icon
                  type="info"
                  :size="8"
                  class="mb-1"
                  color="primary"
                  variant="base"
                />
              </template>
              <template #hover-content>
                <span
                  v-html="
                    'Email address is pre-populated from your profile and can’t be modified.'
                  "
                />
              </template>
            </tooltip>
            <text-field
              v-model="getCurrentUserEmail"
              input-type="text"
              height="40"
              :disabled="true"
              :required="true"
              class="disabledColor"
            />
          </div>
          <div class="pt-2 text-body-1">
            What categories do you wish to receive?
          </div>
          <div>
            <v-treeview
              v-model="tree"
              :items="alertsSectionGroup"
              item-key="show"
              open-all
              disabled
              class="header-class"
            >
              <template v-slot:append="{ item }">
                <hux-switch
                  v-if="item.name != 'Categories'"
                  v-model="item.show"
                  false-color="var(--v-black-lighten4)"
                  :width="item.show ? '80px' : '100px'"
                  :switch-labels="switchLabel"
                  :class="item.show ? 'w-75' : 'w-97'"
                />
              </template>
              <template v-slot:label="{ item }">
                <span
                  :class="
                    item.name != 'Categories'
                      ? 'text-body-1'
                      : 'text-body-2 black--text text--lighten-4'
                  "
                  :data-type="item.type"
                  >{{ item.name }}</span
                >
              </template>
            </v-treeview>
          </div>
        </div>
        <div v-else>
          <v-alert outlined tile class="yellow lighten-1 black--text h-60">
            <div class="d-flex align-center">
              <div class="mr-3 mt-n2">
                <icon type="bulb" :size="36" color="yellow" />
              </div>
              <p class="text-body-1 ma-0 mt-n3">
                You have opted out from receiving alerts &amp; notifications.
              </p>
            </div>
          </v-alert>
        </div>
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
          data-e2e="save"
          @click="closeDrawer"
        >
          Save
        </hux-button>
      </div>
    </template>
  </drawer>
</template>

<script>
import Drawer from "@/components/common/Drawer"
import Icon from "@/components/common/Icon"
import HuxSwitch from "@/components/common/Switch.vue"
import TextField from "@/components/common/TextField.vue"
import { mapGetters } from "vuex"
import Tooltip from "@/components/common/Tooltip.vue"
import HuxButton from "@/components/common/huxButton.vue"

export default {
  name: "AlertConfigureDrawer",
  components: {
    Drawer,
    Icon,
    HuxSwitch,
    TextField,
    Tooltip,
    HuxButton,
  },

  props: {
    value: {
      type: Boolean,
      required: true,
      default: false,
    },
    users: {
      type: Array,
      required: false,
      default: () => [],
    },
  },
  data() {
    return {
      localDrawer: this.value,
      showAlerts: true,
      tree: null,
      switchLabelFullAlerts: [
        {
          condition: true,
          label: "YES",
        },
        {
          condition: false,
          label: "NO",
        },
      ],
      switchLabel: [
        {
          condition: true,
          label: "OPT IN",
        },
        {
          condition: false,
          label: "OPT OUT",
        },
      ],
      alertsSectionGroup: [
        {
          name: "Categories",
          type: "header",
          show: true,
          id: 1,
          children: [
            {
              name: "Data management",
              type: "header",
              show: true,
              id: 2,
              children: [
                {
                  name: "Data sources",
                  type: "header",
                  show: true,
                  id: 3,
                  children: [
                    {
                      name: "Error",
                      type: "child",
                      id: 4,
                      show: true,
                    },
                    {
                      name: "Success",
                      type: "child",
                      id: 5,
                      show: true,
                    },
                    {
                      name: "Informational",
                      type: "child",
                      show: true,
                      id: 6,
                    },
                  ],
                },
                {
                  name: "Identity resolution",
                  type: "header",
                  show: true,
                  id: 7,
                  children: [
                    {
                      name: "Error",
                      type: "child",
                      show: true,
                      id: 8,
                    },
                    {
                      name: "Success",
                      type: "child",
                      show: true,
                      id: 9,
                    },
                    {
                      name: "Informational",
                      type: "child",
                      show: true,
                      id: 10,
                    },
                  ],
                },
              ],
            },
            {
              name: "Decisioning",
              type: "header",
              show: true,
              id: 11,
              children: [
                {
                  name: "Models",
                  type: "header",
                  show: true,
                  id: 12,
                  children: [
                    {
                      name: "Error",
                      type: "child",
                      show: true,
                      id: 13,
                    },
                    {
                      name: "Success",
                      type: "child",
                      show: true,
                      id: 14,
                    },
                    {
                      name: "Informational",
                      type: "child",
                      show: true,
                      id: 15,
                    },
                  ],
                },
              ],
            },
            {
              name: "Orchestration",
              type: "header",
              show: true,
              id: 16,
              children: [
                {
                  name: "Destinations",
                  type: "header",
                  show: true,
                  id: 17,
                  children: [
                    {
                      name: "Error",
                      type: "child",
                      show: true,
                      id: 18,
                    },
                    {
                      name: "Success",
                      type: "child",
                      show: true,
                      id: 19,
                    },
                    {
                      name: "Informational",
                      type: "child",
                      show: true,
                      id: 20,
                    },
                  ],
                },
                {
                  name: "Delivery",
                  type: "header",
                  show: true,
                  id: 21,
                  children: [
                    {
                      name: "Error",
                      type: "child",
                      show: true,
                      id: 22,
                    },
                    {
                      name: "Success",
                      type: "child",
                      show: true,
                      id: 23,
                    },
                    {
                      name: "Informational",
                      type: "child",
                      show: true,
                      id: 24,
                    },
                  ],
                },
                {
                  name: "Audiences",
                  type: "header",
                  show: true,
                  id: 25,
                  children: [
                    {
                      name: "Error",
                      type: "child",
                      show: true,
                      id: 26,
                    },
                    {
                      name: "Success",
                      type: "child",
                      show: true,
                      id: 27,
                    },
                    {
                      name: "Informational",
                      type: "child",
                      show: true,
                      id: 28,
                    },
                  ],
                },
                {
                  name: "Engagements",
                  type: "header",
                  show: true,
                  id: 29,
                  children: [
                    {
                      name: "Error",
                      type: "child",
                      show: true,
                      id: 30,
                    },
                    {
                      name: "Success",
                      type: "child",
                      show: true,
                      id: 31,
                    },
                    {
                      name: "Informational",
                      type: "child",
                      show: true,
                      id: 32,
                    },
                  ],
                },
              ],
            },
          ],
        },
      ],
    }
  },

  computed: {
    ...mapGetters({
      getCurrentUserEmail: "users/getEmailAddress",
    }),

    getNotificationPreferences() {
      return {
        data_sources: ["Informational", "Success", "Error"],
        engagements: ["Informational", "Success", "Error"],
        audiences: ["Informational", "Success", "Error"],
        delivery: ["Error"],
        identity_resolution: ["Informational"],
        models: ["Informational", "Success", "Error"],
        destinations: ["Informational", "Success", "Error"],
      }
    },
  },

  watch: {
    value: function () {
      this.localDrawer = this.value
    },
    localDrawer: function () {
      this.$emit("input", this.localDrawer)
    },
    tree: function () {
      console.log("tree", this.tree)
    },
  },
  methods: {
    toggleAccessFullAlerts(val) {
      this.showAlerts = val
    },
    toggleAccessIndivisualAlerts(e, val) {
      val.show = e
    },
    closeDrawer() {
      this.localDrawer = false
    },
  },
}
</script>
<style lang="scss" scoped>
.black-border {
  border-radius: 50%;
  border: 0.5px solid var(--v-black-base);
}
.full-alert {
  justify-content: space-between;
  align-items: center;
  height: 40px;
}
.w-53 {
  width: 53px;
}
.w-75 {
  width: 75px;
}
.w-97 {
  width: 97px;
}
.disabledColor .v-input__slot {
  background-color: var(--v-primary-lighten1) !important;
}
.h-77 {
  height: 77px;
}
.h-60 {
  height: 60px;
}
::v-deep .v-treeview .v-treeview-node__root {
  border-top: 1px solid var(--v-black-lighten2);
  height: 45px;
  padding: 0;
}
::v-deep .v-treeview-node__root:first {
  border-top: none;
}
::v-deep .v-treeview-node__toggle {
  display: none;
}
::v-deep .v-treeview-node__content {
  padding: 10px 24px 11px 16px;
  height: 45px;
  margin-left: 0 !important;
}
.header-class {
  border: 1px solid var(--v-black-lighten2);
  border-radius: 12px;
}
</style>
