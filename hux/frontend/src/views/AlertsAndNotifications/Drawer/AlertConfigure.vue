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
            @input="toggleAccessFullAlerts($event, item)"
          />
        </div>
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
          <!-- <v-list>
            <v-list-item-group v-model="model">
              <v-list-item v-for="(item, i) in alertsSectionGroup" :key="i">
                <v-list-item-content class="d-flex full-alert">
                  <v-list-item-title v-text="item.name"></v-list-item-title>
                  <hux-switch
                    v-model="showAlerts"
                    false-color="var(--v-black-lighten4)"
                    :width="showAlerts ? '57px' : '60px'"
                    :switch-labels="switchLabel"
                    class="w-53"
                    @input="toggleAccess($event, item)"
                  />
                </v-list-item-content>
              </v-list-item>
            </v-list-item-group>
          </v-list> -->
          <v-treeview
            v-model="tree"
            :items="alertsSectionGroup"
            activatable
            item-key="show"
            open-all
          >
            <template v-slot:append="{ item }">
              <hux-switch
                v-model="item.show"
                false-color="var(--v-black-lighten4)"
                width="100px"
                :switch-labels="switchLabel"
                class="w-89"
              />
            </template>
          </v-treeview>
        </div>
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

export default {
  name: "AlertConfigureDrawer",
  components: {
    Drawer,
    Icon,
    HuxSwitch,
    TextField,
    Tooltip,
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
          name: "Category",
          type: "header",
          show: true,
          children: [
            {
              name: "Data management",
              type: "header",
              show: true,
              children: [
                {
                  name: "Data sources",
                  type: "header",
                  show: true,
                  children: [
                    {
                      name: "Error",
                      type: "child",
                      show: true,
                    },
                    {
                      name: "Success",
                      type: "child",
                      show: true,
                    },
                    {
                      name: "Informational",
                      type: "child",
                      show: true,
                    },
                  ],
                },
                {
                  name: "Identity resolution",
                  type: "header",
                  show: true,
                  children: [
                    {
                      name: "Error",
                      type: "child",
                      show: true,
                    },
                    {
                      name: "Success",
                      type: "child",
                      show: true,
                    },
                    {
                      name: "Informational",
                      type: "child",
                      show: true,
                    },
                  ],
                },
              ],
            },
            {
              name: "Decisioning",
              type: "header",
              show: true,
              children: [
                {
                  name: "Models",
                  type: "header",
                  show: true,
                  children: [
                    {
                      name: "Error",
                      type: "child",
                      show: true,
                    },
                    {
                      name: "Success",
                      type: "child",
                      show: true,
                    },
                    {
                      name: "Informational",
                      type: "child",
                      show: true,
                    },
                  ],
                },
              ],
            },
            {
              name: "Orchestration",
              type: "header",
              show: true,
              children: [
                {
                  name: "Destinations",
                  type: "header",
                  show: true,
                  children: [
                    {
                      name: "Error",
                      type: "child",
                      show: true,
                    },
                    {
                      name: "Success",
                      type: "child",
                      show: true,
                    },
                    {
                      name: "Informational",
                      type: "child",
                      show: true,
                    },
                  ],
                },
                {
                  name: "Delivery",
                  type: "header",
                  show: true,
                  children: [
                    {
                      name: "Error",
                      type: "child",
                      show: true,
                    },
                    {
                      name: "Success",
                      type: "child",
                      show: true,
                    },
                    {
                      name: "Informational",
                      type: "child",
                      show: true,
                    },
                  ],
                },
                {
                  name: "Audiences",
                  type: "header",
                  show: true,
                  children: [
                    {
                      name: "Error",
                      type: "child",
                      show: true,
                    },
                    {
                      name: "Success",
                      type: "child",
                      show: true,
                    },
                    {
                      name: "Informational",
                      type: "child",
                      show: true,
                    },
                  ],
                },
                {
                  name: "Engagements",
                  type: "header",
                  show: true,
                  children: [
                    {
                      name: "Error",
                      type: "child",
                      show: true,
                    },
                    {
                      name: "Success",
                      type: "child",
                      show: true,
                    },
                    {
                      name: "Informational",
                      type: "child",
                      show: true,
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
  },
  methods: {
    toggleAccessFullAlerts(val) {
      this.showAlerts = val
    },
    toggleAccessIndivisualAlerts(val) {
      this.showAlerts = val
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
.w-89 {
  width: 89px;
}
.disabledColor .v-input__slot {
  background-color: var(--v-primary-lighten1) !important;
}
.h-77 {
  height: 77px;
}
</style>
