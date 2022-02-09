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
                  @change="formatFinalResponse($event, item)"
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
                  >{{ item.label }}</span
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
import { mapActions, mapGetters } from "vuex"
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
      //   {
      //     label: "Categories",
      //     name: "categories",
      //     show: true,
      //     children: [
      //       {
      //         label: "Data management",
      //         name: "data_management",
      //         parent: null,
      //         show: true,
      //         children: [
      //           {
      //             label: "Data sources",
      //             name: "datasources",
      //             parent: "data_management",
      //             show: true,
      //             isDeepChild: false,
      //             children: [
      //               {
      //                 label: "Critical",
      //                 name: "critical",
      //                 parent: "datasources",
      //                 show: true,
      //                 isDeepChild: true,
      //               },
      //               {
      //                 label: "Success",
      //                 name: "success",
      //                 parent: "datasources",
      //                 show: true,
      //                 isDeepChild: true,
      //               },
      //               {
      //                 label: "Informational",
      //                 name: "informational",
      //                 parent: "datasources",
      //                 show: true,
      //                 isDeepChild: true,
      //               },
      //             ],
      //           },
      //           {
      //             label: "Identity resolution",
      //             name: "identity_resolution",
      //             parent: "data_management",
      //             show: true,
      //             isDeepChild: false,
      //             children: [
      //               {
      //                 label: "Critical",
      //                 name: "critical",
      //                 parent: "identity_resolution",
      //                 show: true,
      //                 isDeepChild: true,
      //               },
      //               {
      //                 label: "Success",
      //                 name: "success",
      //                 parent: "identity_resolution",
      //                 show: true,
      //                 isDeepChild: true,
      //               },
      //               {
      //                 label: "Informational",
      //                 name: "informational",
      //                 parent: "identity_resolution",
      //                 show: true,
      //                 isDeepChild: true,
      //               },
      //             ],
      //           },
      //         ],
      //       },
      //       {
      //         label: "Decisioning",
      //         name: "decisioning",
      //         parent: null,
      //         show: true,
      //         children: [
      //           {
      //             label: "Models",
      //             name: "models",
      //             parent: "decisioning",
      //             show: true,
      //             isDeepChild: false,
      //             children: [
      //               {
      //                 label: "Critical",
      //                 name: "critical",
      //                 parent: "models",
      //                 show: true,
      //                 isDeepChild: true,
      //               },
      //               {
      //                 label: "Success",
      //                 name: "success",
      //                 parent: "models",
      //                 show: true,
      //                 isDeepChild: true,
      //               },
      //               {
      //                 label: "Informational",
      //                 name: "informational",
      //                 parent: "models",
      //                 show: true,
      //                 isDeepChild: true,
      //               },
      //             ],
      //           },
      //         ],
      //       },
      //       {
      //         label: "Orchestration",
      //         name: "orchestration",
      //         parent: null,
      //         show: true,
      //         children: [
      //           {
      //             label: "Destinations",
      //             name: "destinations",
      //             parent: "orchestration",
      //             isDeepChild: false,
      //             show: true,
      //             children: [
      //               {
      //                 label: "Critical",
      //                 name: "critical",
      //                 parent: "destinations",
      //                 show: true,
      //                 isDeepChild: true,
      //               },
      //               {
      //                 label: "Success",
      //                 name: "success",
      //                 parent: "destinations",
      //                 show: true,
      //                 isDeepChild: true,
      //               },
      //               {
      //                 label: "Informational",
      //                 name: "informational",
      //                 parent: "destinations",
      //                 show: true,
      //                 isDeepChild: true,
      //               },
      //             ],
      //           },
      //           {
      //             label: "Delivery",
      //             name: "delivery",
      //             parent: "orchestration",
      //             show: true,
      //             isDeepChild: false,
      //             children: [
      //               {
      //                 label: "Critical",
      //                 name: "critical",
      //                 parent: "delivery",
      //                 isDeepChild: true,
      //                 show: true,
      //                 isDeepChild: true,
      //               },
      //               {
      //                 label: "Success",
      //                 name: "success",
      //                 parent: "delivery",
      //                 isDeepChild: true,
      //                 show: true,
      //                 isDeepChild: true,
      //               },
      //               {
      //                 label: "Informational",
      //                 name: "informational",
      //                 parent: "delivery",
      //                 isDeepChild: true,
      //                 show: true,
      //                 isDeepChild: true,
      //               },
      //             ],
      //           },
      //           {
      //             label: "Audiences",
      //             name: "audiences",
      //             parent: "orchestration",
      //             show: true,
      //             isDeepChild: false,
      //             children: [
      //               {
      //                 label: "Critical",
      //                 name: "critical",
      //                 parent: "audiences",
      //                 show: true,
      //                 isDeepChild: true,
      //               },
      //               {
      //                 label: "Success",
      //                 name: "success",
      //                 parent: "audiences",
      //                 show: true,
      //                 isDeepChild: true,
      //               },
      //               {
      //                 label: "Informational",
      //                 name: "informational",
      //                 parent: "audiences",
      //                 show: true,
      //                 isDeepChild: true,
      //               },
      //             ],
      //           },
      //           {
      //             label: "Engagements",
      //             name: "engagements",
      //             parent: "orchestration",
      //             show: true,
      //             isDeepChild: false,
      //             children: [
      //               {
      //                 label: "Critical",
      //                 name: "critical",
      //                 parent: "engagements",
      //                 show: true,
      //                 isDeepChild: true,
      //               },
      //               {
      //                 label: "Success",
      //                 name: "success",
      //                 parent: "engagements",
      //                 show: true,
      //                 isDeepChild: true,
      //               },
      //               {
      //                 label: "Informational",
      //                 name: "informational",
      //                 parent: "engagements",
      //                 show: true,
      //                 isDeepChild: true,
      //               },
      //             ],
      //           },
      //         ],
      //       },
      //     ],
      //   },
      // ],
      preferencesMapping: {
        orchestration: ["delivery", "audiences", "destinations", "engagements"],
        decisioning: ["models"],
        data_management: ["identity_resolution", "datasources"],
      },
    }
  },

  computed: {
    ...mapGetters({
      getCurrentUserEmail: "users/getEmailAddress",
    }),

    getNotificationPreferences() {
      return {
        orchestration: ["delivery", "audiences", "destinations", "engagements"],
        decisioning: ["models"],
        data_management: ["identity_resolution", "datasources"],

        // data_sources: ["Informational", "Success", "Critical"],
        // engagements: ["Informational", "Success", "Critical"],
        // audiences: ["Informational", "Success", "Critical"],
        // delivery: ["Critical"],
        // identity_resolution: ["Informational"],
        // models: ["Informational", "Success", "Critical"],
        // destinations: ["Informational", "Success", "Critical"],

        // preferencesMapping: [

        // ]
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
  mounted() {
    console.log("sss")
  },

  updated() {
        this.mapAlertSectionGroups()
    this.$nextTick(function () {
      document
        .getElementsByClassName("v-treeview-node")
        .forEach((element, index) => {
          if (element.childNodes.length == 2) {
            let elem = element.childNodes[0]
            if (index == 0) {
              elem.style["border-top"] = "none"
              elem.style["min-height"] = "30px"
              elem.style["height"] = "30px"
            }
            elem.style["background"] = "#F9FAFB"
          }
        })
    })


    // let tempObj = {
    //   amazing: {
    //     informational: true,
    //     success: false,
    //     critical: false,
    //   },
    // }

    // for (const [key, value] of Object.entries(tempObj)) {
    //   console.log(`${key}: ${value}`)
    // }

    //  this.alertsSectionGroup[0].children.push()
    //  console.log(this.alertsSectionGroup)
  },
  methods: {
    ...mapActions({
      updateUserPreferences: "users/updateUserPreferences",
    }),
    toggleAccessFullAlerts(val) {
      this.showAlerts = val
    },
    toggleAccessIndivisualAlerts(e, val) {
      val.show = e
      // this.formatFinalResponse()
    },
    closeDrawer() {
      this.localDrawer = false
      this.updateUserPreferences(this.updatedConfiguration)
    },
    mapAlertSectionGroups() {
      let currentEmail = "samsingh@deloitte.com"
      let currentUser = this.users.find((data) => data.email == currentEmail)
      this.currentAlertConf = currentUser.alerts
    //  console.log(this.currentAlertConf)

      this.setAlertConfiguration()
    },
    recursiveBinding(data, alerts) {
      let parentData = data.children
      for (let i = 0; i < parentData.length; i++) {
        alerts[parentData[i].name] = {}
        if (parentData[i].show && !parentData[i].isDeepChild) {
          this.recursiveBinding(parentData[i], alerts[parentData[i].name])
        } else if (!parentData[i].show && !parentData[i].isDeepChild) {
          alerts[parentData[i].name] = {}
        } else {
       //   console.log(alerts[parentData[i]])
          alerts[parentData[i].name] = parentData[i].show
        }
      }
      return alerts
    },
    formatFinalResponse(value, item) {
      this.updatedConfiguration = {}
      this.updatedConfiguration.alerts = this.recursiveBinding(this.alertsSectionGroup[0], {})
    },
    checkifDataEmpty() {

    },
    setAllKeyMapping(basicEntity, parentObj) {
         //   console.log('a')
      for (const [key, value] of Object.entries(basicEntity)) {
        if (typeof value === 'object' ) {
          let childObj = {
            label: this.$options.filters.TitleCase(key),
            name: key,
            show: this.checkOptStatus(value),
            isDeepChild: false,
            children: []
          }
        //  console.log(value)
          parentObj.children.push(childObj)
          this.setAllKeyMapping(value, childObj)
        } else {
            let childObj = {
            label: this.$options.filters.TitleCase(key),
            name: key,
            show: value,
            isDeepChild: true,
          }
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
          children: []
      }
      this.setAllKeyMapping(this.currentAlertConf, parentObj)
     this.alertsSectionGroup = [parentObj]
   //   console.log( this.alertsSectionGroup)
     // console.log(this.setAllKeyMapping(this.currentAlertConf, parentObj))
    },
    checkOptStatus(value) {
      let convertedValue = JSON.stringify(value)
      return convertedValue.indexOf('true') != -1 ? true : false
    }
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
</style>
