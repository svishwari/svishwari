<template>
  <drawer
    v-model="localDrawer"
    :content-padding="'pa-0'"
    :content-header-padding="'px-3'"
  >
    <template #header-left>
      <div class="d-flex align-center">
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
            @change="toggleMainSwitch($event)"
          />
        </div>
        <div v-if="showAlerts">
          <div class="pb-4 h-77">
            <tooltip max-width="300px" position-top>
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
                  v-bind.prop="
                    formatInnerHTML(
                      'Email address is pre-populated from your profile and can’t be modified.'
                    )
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
          <div class="pt-2 text-body-1 mb-2">
            What categories do you wish to receive?
          </div>
          <div>
            <v-treeview
              v-if="alertsSectionGroup.length != 0"
              v-model="tree"
              :items="alertsSectionGroup"
              item-key="show"
              open-all
              disabled
              class="header-class"
            >
              <template v-slot:append="{ item }">
                <hux-switch
                  v-if="item.name != 'categories'"
                  v-model="item.show"
                  false-color="var(--v-black-lighten4)"
                  :width="item.show ? '80px' : '100px'"
                  :switch-labels="switchLabel"
                  :class="item.show ? 'w-75' : 'w-97'"
                  @change="toggleIndividualSwitch($event, item)"
                />
              </template>
              <template v-slot:label="{ item }">
                <span
                  :class="
                    item.name != 'categories'
                      ? 'text-body-1'
                      : 'text-body-2 black--text text--lighten-4'
                  "
                  :data-type="item.type"
                  >{{ item.label | TitleCase }}</span
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
          @click="saveChanges"
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
import { mapActions, mapGetters } from "vuex"
import { formatText, formatInnerHTML } from "@/utils"
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
  },
  data() {
    return {
      localDrawer: this.value,
      currentAlertConf: {},
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
      updatedConfiguration: {},
      alertsSectionGroup: [],
    }
  },

  computed: {
    ...mapGetters({
      getCurrentUserEmail: "users/getEmailAddress",
      getAlerts: "users/getUserAlerts",
    }),
  },

  watch: {
    value: function () {
      this.localDrawer = this.value
    },
    localDrawer: function () {
      this.$emit("input", this.localDrawer)
    },
    users: function () {
      this.updateUsers()
    },
  },
  mounted() {
    this.setDefaultConfig()
  },
  updated() {
    if (this.localDrawer) {
      this.mapAlertSectionGroups()
      this.maintainTreeStyles()
    }
  },
  methods: {
    ...mapActions({
      updateUserPreferences: "users/updateUserPreferences",
      getUsersNoti: "notifications/getAllUsers",
    }),
    formatInnerHTML: formatInnerHTML,
    async updateUsers() {
      await this.getUsersNoti()
    },
    closeDrawer() {
      this.localDrawer = false
    },
    saveChanges() {
      this.localDrawer = false
      this.formatFinalResponse()
      this.updateUserPreferences(this.updatedConfiguration)
      this.$emit("onDrawerClose")
    },
    maintainTreeStyles() {
      this.$nextTick(function () {
        document
          .getElementsByClassName("v-treeview-node")
          .forEach((element, index) => {
            if (element.childNodes.length == 2) {
              let elem = element.childNodes[0]
              if (index == 0) {
                elem.style["border-top"] = "none"
                elem.style["border-top-left-radius"] = "12px"
                elem.style["border-top-right-radius"] = "12px"
                elem.style["min-height"] = "30px"
                elem.style["height"] = "30px"
              }
              elem.style["background"] = "#F9FAFB"
            }
          })
      })
    },
    mapAlertSectionGroups() {
      this.currentAlertConf = this.getAlerts
      if (this.checkIfconfigExited(this.currentAlertConf)) {
        this.setAlertConfiguration()
      } else {
        this.showAlerts = false
      }
    },
    // Recursion for setting nested output structure
    recursiveBinding(data, alerts) {
      let parentData = data.children
      for (let i = 0; i < parentData.length; i++) {
        alerts[parentData[i].name] = {}
        if (parentData[i].show && !parentData[i].isDeepChild) {
          this.recursiveBinding(parentData[i], alerts[parentData[i].name])
        } else if (!parentData[i].show && !parentData[i].isDeepChild) {
          alerts[parentData[i].name] = {}
        } else {
          alerts[parentData[i].name] = parentData[i].show
        }
      }
      return alerts
    },

    checkIfconfigExited(entity) {
      return entity ? Object.keys(entity).length !== 0 : false
    },

    toggleIndividualSwitch(event, item) {
      this.manualToggleChanges(event, item)
      this.formatFinalResponse()
      this.maintainTreeStyles()
    },

    formatFinalResponse() {
      this.updatedConfiguration = {}
      this.updatedConfiguration.alerts = this.showAlerts
        ? this.recursiveBinding(this.alertsSectionGroup[0], {})
        : {}
    },

    manualToggleChanges(flag, item) {
      if (item && !item.isDeepChild) {
        item.children.forEach((data) => {
          if (data.children.length > 0) {
            // Recursion for setting event flag to deepest level
            data.show = flag
            this.manualToggleChanges(flag, data)
          } else {
            data.show = flag
          }
        })
      }
    },

    toggleMainSwitch(value) {
      if (value) {
        this.setDefaultConfig()
      } else {
        this.updatedConfiguration = {}
      }
      this.maintainTreeStyles()
    },

    // Recursion for getting nested input structure
    setAllKeyMapping(basicEntity, parentObj) {
      for (const [key, value] of Object.entries(basicEntity)) {
        let childObj = {
          label: formatText(key),
          name: key,
          isDeepChild: false,
          children: [],
        }
        if (typeof value === "object") {
          childObj.show = this.checkOptStatus(value)
          childObj.isDeepChild = false
          childObj.children = []
          parentObj.children.push(childObj)
          this.setAllKeyMapping(value, childObj)
        } else {
          childObj.show = value
          childObj.isDeepChild = true
          parentObj.children.push(childObj)
        }
      }
      return parentObj
    },
    setAlertConfiguration() {
      let parentObj = {
        label: "Categories",
        name: "categories",
        show: true,
        children: [],
      }
      this.setAllKeyMapping(this.currentAlertConf, parentObj)
      this.alertsSectionGroup = [parentObj]
    },
    checkOptStatus(value) {
      let convertedValue = JSON.stringify(value)
      return convertedValue.indexOf("true") != -1 ? true : false
    },
    setDefaultConfig() {
      this.alertsSectionGroup = [
        {
          label: "Categories",
          name: "categories",
          show: true,
          children: [
            {
              label: "Data management",
              name: "data_management",
              parent: null,
              show: true,
              children: [
                {
                  label: "Data sources",
                  name: "data_sources",
                  parent: "data_management",
                  show: true,
                  isDeepChild: false,
                  children: [
                    {
                      label: "Critical",
                      name: "critical",
                      parent: "data_sources",
                      show: true,
                      isDeepChild: true,
                    },
                    {
                      label: "Success",
                      name: "success",
                      parent: "data_sources",
                      show: true,
                      isDeepChild: true,
                    },
                    {
                      label: "Informational",
                      name: "informational",
                      parent: "data_sources",
                      show: true,
                      isDeepChild: true,
                    },
                  ],
                },
              ],
            },
            {
              label: "Decisioning",
              name: "decisioning",
              parent: null,
              show: true,
              children: [
                {
                  label: "Models",
                  name: "models",
                  parent: "decisioning",
                  show: true,
                  isDeepChild: false,
                  children: [
                    {
                      label: "Critical",
                      name: "critical",
                      parent: "models",
                      show: true,
                      isDeepChild: true,
                    },
                    {
                      label: "Success",
                      name: "success",
                      parent: "models",
                      show: true,
                      isDeepChild: true,
                    },
                    {
                      label: "Informational",
                      name: "informational",
                      parent: "models",
                      show: true,
                      isDeepChild: true,
                    },
                  ],
                },
              ],
            },
            {
              label: "Orchestration",
              name: "orchestration",
              parent: null,
              show: true,
              children: [
                {
                  label: "Destinations",
                  name: "destinations",
                  parent: "orchestration",
                  isDeepChild: false,
                  show: true,
                  children: [
                    {
                      label: "Critical",
                      name: "critical",
                      parent: "destinations",
                      show: true,
                      isDeepChild: true,
                    },
                    {
                      label: "Success",
                      name: "success",
                      parent: "destinations",
                      show: true,
                      isDeepChild: true,
                    },
                    {
                      label: "Informational",
                      name: "informational",
                      parent: "destinations",
                      show: true,
                      isDeepChild: true,
                    },
                  ],
                },
                {
                  label: "Delivery",
                  name: "delivery",
                  parent: "orchestration",
                  show: true,
                  isDeepChild: false,
                  children: [
                    {
                      label: "Critical",
                      name: "critical",
                      parent: "delivery",
                      show: true,
                      isDeepChild: true,
                    },
                    {
                      label: "Success",
                      name: "success",
                      parent: "delivery",
                      isDeepChild: true,
                      show: true,
                    },
                    {
                      label: "Informational",
                      name: "informational",
                      parent: "delivery",
                      isDeepChild: true,
                      show: true,
                    },
                  ],
                },
                {
                  label: "Audiences",
                  name: "audiences",
                  parent: "orchestration",
                  show: true,
                  isDeepChild: false,
                  children: [
                    {
                      label: "Critical",
                      name: "critical",
                      parent: "audiences",
                      show: true,
                      isDeepChild: true,
                    },
                    {
                      label: "Success",
                      name: "success",
                      parent: "audiences",
                      show: true,
                      isDeepChild: true,
                    },
                    {
                      label: "Informational",
                      name: "informational",
                      parent: "audiences",
                      show: true,
                      isDeepChild: true,
                    },
                  ],
                },
                {
                  label: "Engagements",
                  name: "engagements",
                  parent: "orchestration",
                  show: true,
                  isDeepChild: false,
                  children: [
                    {
                      label: "Critical",
                      name: "critical",
                      parent: "engagements",
                      show: true,
                      isDeepChild: true,
                    },
                    {
                      label: "Success",
                      name: "success",
                      parent: "engagements",
                      show: true,
                      isDeepChild: true,
                    },
                    {
                      label: "Informational",
                      name: "informational",
                      parent: "engagements",
                      show: true,
                      isDeepChild: true,
                    },
                  ],
                },
              ],
            },
          ],
        },
      ]
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
::v-deep .v-text-field__slot {
  input {
    color: var(--v-black-lighten4) !important;
  }
}
::v-deep .v-treeview-node__content {
  .v-treeview-node__label {
    span {
      color: var(--v-black-base) !important;
    }
  }
  .v-treeview-node__append {
    .v-input {
      .v-input__control {
        .v-input__slot {
          .v-input--selection-controls__input {
            .v-input--switch__thumb {
              &:last-child {
                right: 1px !important;
                &.primary--text {
                  right: 0px !important;
                }
              }
            }
          }
        }
      }
    }
  }
}
::v-deep .v-treeview {
  & > .v-treeview-node {
    & > .v-treeview-node__root {
      & > .v-treeview-node__content {
        & > .v-treeview-node__label {
          & > span {
            color: var(--v-black-lighten4) !important;
          }
        }
      }
    }
  }
}
</style>
