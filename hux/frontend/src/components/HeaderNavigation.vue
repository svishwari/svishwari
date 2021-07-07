<template>
  <div class="d-flex">
    <v-menu :min-width="200" left offset-y close-on-click>
      <template #activator="{ on }">
        <span v-on="on" class="d-flex cursor-pointer">
          <v-btn class="mx-2 box-shadow-25" color="white" fab x-small>
            <v-icon color="secondary"> mdi-plus </v-icon>
          </v-btn>
        </span>
      </template>
      <v-list>
        <v-list-item>
          <v-list-item-title class="font-weight-bold"> Add </v-list-item-title>
        </v-list-item>
        <v-list-item
          @click="routerRedirect(link.path)"
          v-for="link in dropdownLinks"
          :key="link.name"
        >
          <v-list-item-title class="text-h6 neroBlack--text">
            {{ link.name }}
          </v-list-item-title>
        </v-list-item>
      </v-list>
    </v-menu>
    <v-menu :min-width="200" left offset-y close-on-click>
      <template #activator="{ on }">
        <span v-on="on" class="d-flex cursor-pointer mr-1">
          <v-btn class="mx-2 box-shadow-25" color="white" fab x-small>
            <v-icon color="secondary"> mdi-bell-outline </v-icon>
            <!-- <span class="notification-count ">{{alertData.length}}</span> -->
          </v-btn>
        </span>
      </template>
      <v-list class="alert-menu-main">
        <v-list-item>
          <v-list-item-title class="font-weight-bold">
            Most recent alerts
          </v-list-item-title>
        </v-list-item>
        <v-list-item v-for="data in alertData" :key="data.id">
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
  </div>
</template>

<script>
import Status from "./common/Status.vue"
import TimeStamp from "./common/huxTable/TimeStamp.vue"
export default {
  name: "HeaderNavigation",
  components: {
    Status,
    TimeStamp,
  },
  data() {
    return {
      dropdownLinks: [
        { name: "Data Source", path: "DataSourceConfiguration" },
        { name: "Destination", path: "DestinationConfiguration" },
        { name: "Audience", path: "AudienceConfiguration" },
        { name: "Engagement", path: "EngagementConfiguration" },
      ],
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
  methods: {
    routerRedirect(path) {
      this.$router.push({ name: path, query: { select: true } })
    },
    alertRouters() {
      this.$router.push({ name: "AlertsAndNotifications" })
    },
  },
}
</script>

<style lang="scss" scoped>
.v-menu__content {
  .alert-menu-main {
    top: 64px !important;
    width: 296px !important;
    height: 283px !important;
    overflow-wrap: break-word !important;
  }
}
.v-menu__content {
  top: 64px !important;
  .v-list {
    .v-list-item {
      min-height: 40px !important;
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
// .notification-count {
//     color: white;
//     margin-bottom: 10px;
//     border: 1px solid red;
//     border-radius: 50px;
//     background-color: red;
//     margin-left: -5px;
// }
</style>
