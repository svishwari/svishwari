<template>
  <v-menu :min-width="200" left offset-y close-on-click>
    <template #activator="{ on }">
      <span class="d-flex cursor-pointer" v-on="on">
        <v-btn
          class="mx-2 box-shadow-25"
          data-e2e="notification-bell"
          color="white"
          fab
          x-small
        >
          <v-icon color="primary"> mdi-bell-outline </v-icon>
        </v-btn>
      </span>
    </template>
    <v-list class="alert-menu-main">
      <v-list-item>
        <v-list-item-title class="font-weight-bold">
          Most recent alerts
        </v-list-item-title>
      </v-list-item>
      <div class="notification-div">
        <v-list-item
          v-for="data in mostRecentNotifications"
          :key="data.id"
          data-e2e="notification-item"
        >
          <v-list-item-title
            class="text-h6 black--text text--darken-4 list-main"
          >
            <div class="d-flex text-caption">
              <status
                :status="data.notification_type"
                :show-label="false"
                :icon-size="17"
              />
              <tooltip>
                <template #label-content>
                  <span class="wrap-word">
                    {{ data.description }}
                  </span>
                </template>
                <template #hover-content>
                  <span> {{ data.description }} </span>
                </template>
              </tooltip>
            </div>
            <div class="list-stamp">
              <time-stamp :value="data.created" />
            </div>
          </v-list-item-title>
        </v-list-item>
      </div>
      <v-list-item>
        <v-list-item-title>
          <router-link
            :to="{
              name: 'AlertsAndNotifications',
            }"
            class="text-h6 view-all text-decoration-none"
          >
            View all alerts
          </router-link>
        </v-list-item-title>
      </v-list-item>
    </v-list>
  </v-menu>
</template>

<script>
import { mapActions, mapGetters } from "vuex"
import { orderBy } from "lodash"
import Status from "./common/Status.vue"
import Tooltip from "./common/Tooltip.vue"
import TimeStamp from "./common/huxTable/TimeStamp.vue"

export default {
  name: "Notification",
  components: {
    Status,
    TimeStamp,
    Tooltip,
  },
  data() {
    return {
      batchDetails: {
        batchSize: 5,
        batchNumber: 1,
        isLazyLoad: false,
      },
    }
  },
  computed: {
    ...mapGetters({
      notifications: "notifications/list",
    }),
    mostRecentNotifications() {
      return orderBy(this.notifications, "created", "desc").slice(
        0,
        this.batchDetails.batchSize
      )
    },
  },
  async mounted() {
    this.$root.$on("refresh-notifications", async () => {
      await this.getAllNotifications(this.batchDetails)
    })
    await this.getAllNotifications(this.batchDetails)
  },
  methods: {
    ...mapActions({
      getAllNotifications: "notifications/getAll",
    }),
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
.list-main {
  margin-bottom: 22px !important;
}
.v-menu__content {
  top: 64px !important;
  overflow-y: hidden !important;
  .alert-menu-main {
    width: 296px !important;
    height: 283px !important;
    overflow-wrap: break-word !important;
  }
}
.notification-div {
  overflow-y: auto !important;
  height: 170px !important;
}
.view-all {
  font-family: Open Sans;
  font-style: normal;
  font-weight: normal;
  font-size: 14px;
  line-height: 22px;
  color: var(--v-primary-base) !important;
  cursor: pointer;
}
::v-deep .v-list-item__title,
.v-list-item__subtitle {
  flex: 8 1 127%;
  overflow: unset !important;
  text-overflow: ellipsis;
  white-space: revert !important;
}
.wrap-word {
  max-width: 215px !important;
  display: -webkit-box;
  -webkit-box-orient: vertical !important;
  -webkit-line-clamp: 3 !important;
  overflow: hidden !important;
}
</style>
