
<template>
 <v-menu :min-width="200" left offset-y close-on-click>
     <template #activator="{ on }">
        <span v-on="on" class="d-flex cursor-pointer">
          <v-btn class="mx-2 box-shadow-25" color="white" fab x-small>
            <v-icon color="secondary"> mdi-bell-outline </v-icon>
          </v-btn>
        </span>
      </template>
        <v-list class="alert-menu-main">
        <v-list-item>
          <v-list-item-title class="font-weight-bold">
            Most recent alerts
          </v-list-item-title>
        </v-list-item>
        <v-list-item v-for="data in getNotificationData" :key="data.id">
          <v-list-item-title class="text-h6 neroBlack--text list-main">
            <div class="d-flex list-desc">
              <status
                :status="data.type"
                :showLabel="false"
                class="status-icon"
                :iconSize="17"
              />
              <span> {{ data.description }} </span>
            </div>
            <div class="list-stamp">
              <time-stamp :value="data.time" />
            </div>
          </v-list-item-title>
        </v-list-item>
        <v-list-item>
          <v-list-item-title class="text-h6 neroBlack--text">
            <a @click="alertRouters()">View all alerts</a>
          </v-list-item-title>
        </v-list-item>
      </v-list>
  </v-menu>
  
</template>

<script>
import { mapActions, mapGetters } from "vuex"
import Status from "./common/Status.vue"
import TimeStamp from "./common/huxTable/TimeStamp.vue"
export default {
  name: "Notification",
    components: {
    Status,
    TimeStamp
  },
  data(){
    return {
      alertData: [
        {
          id: 1,
          time: "2021-07-04T09:41:22.237Z",
          type: "Success",
          description: "Data Source CS005 lost connection.",
          category: "Orchestration",
        },
        {
          id: 2,
          time: "2021-07-04T09:41:22.237Z",
          type: "Feedback",
          description: "Facebook delivery stopped.",
          category: "Decisioning",
        },
        {
          id: 3,
          time: "2021-07-04T09:41:22.237Z",
          type: "Critical",
          description:
            "Data Source CS004 lost connectivity. This is an example of a longer description that needs to be cut off.",
          category: "Data management",
        },
      ],
    }
  },
    computed: {
    ...mapGetters({
      notification: "notification/list",
    }),
    getNotificationData(){
      return this.notification;
    }
 },
  methods: {
     ...mapActions({
      getNotification: "notification/getAll",
    }),
    alertRouters() {
      this.$router.push({ name: "AlertsAndNotifications" })
    },
  },
  async mounted() {
    await this.getNotification()
  },
}
</script>
<style lang="scss" scoped>
.notification-badge {
  .icon-btn {
    box-shadow: 0px 1px 5px rgb(0 0 0 / 25%);
    &.v-btn {
      &.v-btn--icon {
        &.v-btn--round {
          margin-right: 9px;
          margin-left: 9px;
        }
      }
    }
  }
}
.list-stamp {
  margin-left: 25px;
  margin-top: 5px;
  font-size: 11px;
}
.list-desc {
  font-size: 12px;
}
.list-main {
  margin-bottom: 22px !important;
}
.v-menu__content {
  top: 56px !important;
  .alert-menu-main {
    width: 296px !important;
    height: 283px !important;
    overflow-wrap: break-word !important;
  }
}
</style>
