<template>
  <v-menu
    v-model="batchDetails.menu"
    :min-width="200"
    left
    offset-y
    close-on-click
  >
    <template #activator="{ on }">
      <span class="d-flex cursor-pointer mr-4" v-on="on">
        <tooltip :z-index="99">
          <template #label-content>
            <span :class="{ 'icon-shadow': batchDetails.menu }">
              <icon
                data-e2e="notification-bell"
                class="mx-2 my-2 nav-icon"
                :type="seenNotifications ? 'bell' : 'bell-notification'"
                :size="24"
                :class="{ 'active-icon': batchDetails.menu }"
              />
            </span>
          </template>
          <template #hover-content> Alerts </template>
        </tooltip>
      </span>
    </template>
    <v-list class="alert-menu-main">
      <v-list-item>
        <v-list-item-title class="font-weight-semi-bold text-h6 black--text">
          <span v-if="mostRecentNotifications.length > 0">
            Most recent alerts
          </span>
          <span v-else>No unread alerts </span>
        </v-list-item-title>
      </v-list-item>
      <div class="notification-div">
        <span v-if="mostRecentNotifications.length > 0">
          <v-list-item
            v-for="data in mostRecentNotifications"
            :key="data.id"
            data-e2e="notification-item"
          >
            <v-list-item-title class="text-h6 black--text list-main">
              <div class="d-flex text-caption">
                <status
                  :status="formatText(data.notification_type)"
                  :show-label="false"
                  :icon-size="21"
                />
                <div class="d-flex flex-column">
                  <tooltip>
                    <template #label-content>
                      <span class="wrap-word text-body-2 black--text">
                        {{ data.description }}
                      </span>
                    </template>
                    <template #hover-content>
                      <span> {{ data.description }} </span>
                    </template>
                  </tooltip>
                  <div class="text-body-2 black--text">
                    <time-stamp :value="data.created_time" />
                  </div>
                </div>
              </div>
            </v-list-item-title>
          </v-list-item>
        </span>
      </div>
      <v-list-item>
        <v-list-item-title>
          <router-link
            :to="{
              name: 'AlertsAndNotifications',
            }"
            data-e2e="notifications-view-all"
            class="text-body-1 primary--text view-all text-decoration-none"
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
import { formatText } from "@/utils"
import Status from "./common/Status.vue"
import Tooltip from "./common/Tooltip.vue"
import TimeStamp from "./common/huxTable/TimeStamp.vue"
import Icon from "@/components/common/Icon"

export default {
  name: "Notification",
  components: {
    Status,
    TimeStamp,
    Tooltip,
    Icon,
  },
  data() {
    return {
      batchDetails: {
        batch_size: 5,
        batch_number: 1,
        isLazyLoad: false,
        menu: false,
      },
    }
  },
  computed: {
    ...mapGetters({
      alerts: "alerts/list",
      notifications: "notifications/latest5",
      seenNotifications: "notifications/seenNotifications",
    }),
    mostRecentNotifications() {
      return orderBy(this.notifications, "created_time", "desc").slice(
        0,
        this.batchDetails.batch_size
      )
    },
  },
  watch: {
    alerts() {
      if (this.alerts.length > 0 && this.alerts[0].code == 503) {
        this.$router.push({ name: "ServiceError" })
      }
    },
    $route() {
      this.getLatestNotifications()
    },
  },
  async mounted() {
    this.$root.$on("refresh-notifications", this.getLatestNotifications())
    await this.getAllNotifications(this.batchDetails)
  },
  methods: {
    ...mapActions({
      getAllNotifications: "notifications/getAll",
    }),
    formatText: formatText,
    async getLatestNotifications() {
      await this.getAllNotifications(this.batchDetails)
    },
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
}
.list-main {
  margin-bottom: 22px !important;
}
.v-menu__content {
  margin-left: 70px !important;
  top: 70px !important;
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
.no-data {
  margin-left: 30%;
  position: absolute;
  margin-top: 22%;
}
</style>
