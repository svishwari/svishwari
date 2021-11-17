<template>
  <drawer
    v-model="localDrawer"
    :content-padding="'pa-0'"
    :content-header-padding="'px-3'"
    :expanded-width="300"
    :width="300"
  >
    <template #header-left>
      <span class="text-h2 black--text"> Filter ({{ filterLength }}) </span>
    </template>
    <template #header-right>
      <v-btn
        plain
        :color="filterLength > 0 ? 'primary base' : 'black lighten3'"
        :disabled="filterLength > 0 ? false : true"
        class="text-button float-right clear-btn"
        @click="clearFilter()"
      >
        Clear
      </v-btn>
    </template>

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
            v-for="data in usersData"
            :key="data.id"
            v-model="selctedUsers"
            multiple
            color="#00a3e0"
            :label="data.display_name"
            :value="data.display_name"
          ></v-checkbox>
        </hux-filter-panel>
      </hux-filter-panels>
    </template>
    <template #footer-left>
      <v-btn
        tile
        color="white"
        class="text-button ml-auto"
        @click="localDrawer = false"
      >
        Cancel
      </v-btn>
    </template>
    <template #footer-right>
      <v-btn
        tile
        color="primary"
        class="text-button ml-auto"
        width="134"
        disabled
        @click="apply()"
      >
        Apply filter
      </v-btn>
    </template>
  </drawer>
</template>

<script>
import Drawer from "@/components/common/Drawer"
import HuxFilterPanels from "@/components/common/FilterPanels"
import HuxFilterPanel from "@/components/common/FilterPanel"
export default {
  name: "AlertFilterDrawer",
  components: {
    Drawer,
    HuxFilterPanels,
    HuxFilterPanel,
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
      usersData: this.users,
      selctedAlertType: [],
      selctedCategory: [],
      selectedTimeType: "Last week",
      selctedUsers: [],
      selectedTimeCount: 1,
    }
  },
  computed: {
    filterLength() {
      let alert = this.selctedAlertType.length > 0 ? 1 : 0
      let category = this.selctedCategory.length > 0 ? 1 : 0
      let time = 1
      let users = this.selctedUsers.length > 0 ? 1 : 0
      return alert + category + time + users
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
    getTime(value) {
      let today_date = new Date()
      return new Date(
        today_date.getFullYear(),
        today_date.getMonth(),
        today_date.getDate() - value
      )
    },
    clearFilter() {
      this.selctedAlertType = []
      this.selctedCategory = []
      this.selectedTimeType = "Last week"
      this.selctedUsers = []
    },
    apply() {
      let getTime
      switch (this.selectedTimeType) {
        case "Today":
          getTime = this.getTime(0)
          break
        case "Last week":
          getTime = this.getTime(7)
          break
        case "Last month":
          getTime = this.getTime(30)
          break
        case "Last 3 months":
          getTime = this.getTime(90)
          break
        case "Last 6 months":
          this.getTime(180)
          break
        default:
          this.getTime(7)
          break
      }
      this.$emit("onSectionAction", {
        getTime: this.$options.filters.Date(getTime, "YYYY-MM-DD"),
        selctedAlertType: this.selctedAlertType,
        selctedCategory: this.selctedCategory,
        selctedUsers: this.selctedUsers,
      })
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
.clear-btn {
  padding-left: 7rem !important;
}
</style>
