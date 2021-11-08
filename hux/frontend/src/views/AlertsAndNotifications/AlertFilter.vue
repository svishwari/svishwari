<template>
  <drawer
    v-model="localDrawer"
    :content-padding="'pa-0'"
    :content-header-padding="'px-3'"
    :expanded-width="300"
    :width="300"
  >
    <template #header-left>
      <span class="text-h2 black--text"> Filter (0) </span>
    </template>
    <template #header-right>
      <span class="text---body-2 primary--text"> Clear </span></template
    >
    <template #default>
      <hux-filter-panels>
        <hux-filter-panel title="Alert type" :count="selctedAlertType.length">
          <v-checkbox
            v-for="data in alertType"
            :key="data.id"
            v-model="selctedAlertType"
            multiple
            color="#00a3e0"
            class="text--base-1"
            :label="data.title"
            :value="data.title"
          ></v-checkbox>
        </hux-filter-panel>
        <hux-filter-panel title="Category" :count="selctedCategory.length">
          <v-checkbox
            v-for="data in category"
            :key="data.id"
            v-model="selctedCategory"
            multiple
            color="#00a3e0"
            :label="data.title"
            :value="data.title"
          ></v-checkbox>
        </hux-filter-panel>
        <hux-filter-panel title="Time" :count="1">
          <v-radio-group v-model="selectedTimeType">
            <v-radio
              v-for="data in time"
              :key="data.id"
              :label="data.title"
              color="#00a3e0"
              :value="data.title"
            ></v-radio>
          </v-radio-group>
        </hux-filter-panel>
        <hux-filter-panel title="User" :count="selctedUsers.length">
          <v-checkbox
            v-for="data in users"
            :key="data.id"
            v-model="selctedUsers"
            multiple
            color="#00a3e0"
            :label="data.title"
            :value="data.title"
          ></v-checkbox>
        </hux-filter-panel>
      </hux-filter-panels>
    </template>
    <template #footer-right>
      <v-btn
        tile
        color="primary"
        class="text-button ml-auto"
        width="134"
        @click="apply()"
      >
        Apply filter
      </v-btn>
    </template>
  </drawer>
</template>

<script>
// import { mapGetters } from "vuex"
import Drawer from "@/components/common/Drawer"
// import Icon from "@/components/common/Icon"
import HuxFilterPanels from "@/components/common/FilterPanels"
import HuxFilterPanel from "@/components/common/FilterPanel"
export default {
  name: "AlertFilterDrawer",
  components: {
    Drawer,
    // Icon,
    HuxFilterPanels,
    HuxFilterPanel,
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
      alertType: [
        {
          id: 1,
          title: "Success",
        },
        {
          id: 2,
          title: "Critical",
        },
        {
          id: 3,
          title: "Feedback",
        },
        {
          id: 4,
          title: "Informational",
        },
      ],
      category: [
        {
          id: 1,
          title: "Data sources",
        },
        {
          id: 2,
          title: "Destinations",
        },
        {
          id: 3,
          title: "Engagements",
        },
        {
          id: 4,
          title: "Delivery",
        },
        {
          id: 5,
          title: "Orchestration",
        },
        {
          id: 6,
          title: "Customers",
        },
        {
          id: 7,
          title: "Models",
        },
      ],
      time: [
        {
          id: 1,
          title: "All time",
        },
        {
          id: 2,
          title: "Today",
        },
        {
          id: 3,
          title: "Last week",
        },
        {
          id: 4,
          title: "Last month",
        },
        {
          id: 5,
          title: "Last 3 months",
        },
        {
          id: 6,
          title: "Last 6 months",
        },
      ],
      users: [
        {
          id: 1,
          title: "user 1",
        },
        {
          id: 2,
          title: "user 2",
        },
        {
          id: 3,
          title: "user 3",
        },
        {
          id: 4,
          title: "user 4",
        },
        {
          id: 5,
          title: "user 5",
        },
        {
          id: 6,
          title: "user 6",
        },
      ],
      selctedAlertType: [],
      selctedCategory: [],
      selectedTimeType: "Last week",
      selctedUsers: [],
      selectedTimeCount: 1,
    }
  },
  computed: {},
  watch: {
    value: function () {
      this.localDrawer = this.value
    },
    localDrawer: function () {
      this.$emit("input", this.localDrawer)
    },
  },
  methods: {
    apply() {
      let first_date = new Date()
      if (this.selectedTimeType === "Last week") {
        // let last_date =
      }
      console.log("value", first_date)
    },
  },
}
</script>
<style scoped>
::v-deep.v-input--selection-controls {
  margin-top: 0px !important;
  padding-top: 0px !important;
}
::v-deep.input__slot {
  margin: 0px !important;
}
::v-deep .v-input--selection-controls .v-input__slot {
  margin-bottom: 0px !important;
}
::v-deep.theme--light .v-messages {
  min-height: 6px !important;
  color: var(--v-black-base);
}
</style>
