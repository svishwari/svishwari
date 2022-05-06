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
        <status
          :status="formatText(notificationData.notification_type)"
          :show-label="false"
          class="d-flex"
          :icon-size="32"
        />
        <h3 class="text-h2 ml-1 black--text text--darken-4">
          Alert ID: {{ notificationData.id | Shorten }}
        </h3>
      </div>
    </template>
    <template #default>
      <div
        v-if="notificationData && notificationContent"
        class="pl-7 pt-1 pr-5"
      >
        <div v-for="data in notificationContent" :key="data.id" class="mt-5">
          <div class="text-body-1 black--text">
            {{ data.title }}
          </div>
          <div class="text-body-1 black--text text--lighten-4 mt-1">
            {{ data.value | Empty("-") }}
          </div>
        </div>
      </div>
    </template>
  </drawer>
</template>

<script>
import { mapGetters } from "vuex"
import { formatText } from "@/utils"
import Drawer from "@/components/common/Drawer"
import Status from "@/components/common/Status.vue"

export default {
  name: "AlertDrawer",
  components: {
    Drawer,
    Status,
  },

  props: {
    value: {
      type: Boolean,
      required: true,
      default: false,
    },
    notificationId: {
      type: String,
      required: false,
      default: "",
    },
  },
  data() {
    return {
      localDrawer: this.value,
      notificationData: {},
    }
  },

  computed: {
    ...mapGetters({
      getSingleNotification: "notifications/single",
    }),

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
            title: "Alert object ID",
            value: this.notificationData.id,
          },
          {
            id: 3,
            title: "Category",
            value: formatText(this.notificationData.category),
          },
          {
            id: 4,
            title: "Date",
            value: this.formattedDate(this.notificationData.created),
          },
          {
            id: 5,
            title: "User",
            value: formatText(this.notificationData.username),
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
      if (this.localDrawer) this.updateNotificationData()
    },
  },

  methods: {
    formattedDate(value) {
      if (value) {
        return this.$options.filters.Date(value, "MMM DD, YYYY h:mm A")
      }
      return "-"
    },
    updateNotificationData() {
      this.notificationData = this.getSingleNotification(this.notificationId)
    },
    formatText: formatText,
  },
}
</script>
