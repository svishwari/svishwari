<template>
  <drawer
    v-model="localDrawer"
    :content-padding="'pa-0'"
    :content-header-padding="'px-3'"
  >
    <template #header-left>
      <div
        v-if="
          notificationData &&
          notificationData.notification_type &&
          notificationData.id
        "
        class="d-flex align-center"
      >
        <icon
          :type="
            notificationData.notification_type === 'Success'
              ? 'success_new'
              : notificationData.notification_type
          "
          :size="32"
          :color="getIconColor(notificationData.notification_type)"
          :variant="getIconVariant(notificationData.notification_type)"
          class="d-block mr-2"
        />
        <h3 class="text-h2 ml-1 black--text text--darken-4">
          Alert ID: {{ notificationData.id }}
        </h3>
      </div>
    </template>
    <template #default>
      <div
        v-if="notificationData && notificationContent"
        class="pl-7 pt-1 pr-5"
      >
        <div v-for="data in notificationContent" :key="data.id" class="mt-5">
          <div class="text-body-1 black--text font-weight-semi-bold">
            {{ data.title }}
          </div>
          <div class="text-body-1 black--text text--lighten-4 mt-1">
            {{ data.value }}
          </div>
        </div>
      </div>
    </template>
  </drawer>
</template>

<script>
import { mapGetters } from "vuex"
import Drawer from "@/components/common/Drawer"
import Icon from "@/components/common/Icon"

export default {
  name: "AlertDrawer",
  components: {
    Drawer,
    Icon,
  },

  props: {
    value: {
      type: Boolean,
      required: true,
      default: false,
    },
    alertId: {
      type: String,
      required: false,
      default: "",
    },
  },
  data() {
    return {
      localDrawer: this.value,
    }
  },

  computed: {
    ...mapGetters({
      getSingleNotification: "notifications/single",
    }),

    notificationData() {
      let notification = this.getSingleNotification(this.alertId)
      return notification
    },

    notificationContent() {
      if (this.notificationData) {
        return [
          {
            id: 1,
            title: "Full Description",
            value: this.notificationData.description,
            subLabel: null,
          },
          {
            id: 2,
            title: "Category",
            value: this.notificationData.category,
          },
          {
            id: 3,
            title: "Date",
            value: this.formattedDate(this.notificationData.created),
          },
          {
            id: 4,
            title: "User",
            value: this.notificationData.username,
            subLabel: null,
          },
        ]
      }
      return []
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
    formattedDate(value) {
      if (value) {
        return this.$options.filters.Date(value, "MMM DD, YYYY h:mm A")
      }
      return "-"
    },
    getIconColor(value) {
      if (value) {
        return value === "Success"
          ? "success"
          : value === "Critical"
          ? "error"
          : "primary"
      }
    },

    getIconVariant(value) {
      if (value) {
        return value === "Informational" ? "lighten6" : "base"
      }
    },
  },
}
</script>
