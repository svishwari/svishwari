<template>
  <div class="d-flex align-center">
    <span class="text-body-2 black--text text--lighten-4 mr-2">
      {{ getFormattedTime }}
      <tooltip>
        <template #label-content>
          <span>
            {{ appLoadTime | Date("zzz", (local = true)) | Abbreviation }}
          </span>
        </template>
        <template #hover-content>
          {{ appLoadTime | Date("zzz") }}
        </template>
      </tooltip>
    </span>
    <v-icon size="16" class="mr-9 nav-icon" @click="$router.go()">
      mdi-refresh
    </v-icon>
    <v-menu
      v-if="!clientPanel && role != 'hxtrustid' && getDropdownLinks.length > 0"
      v-model="menu"
      :min-width="200"
      left
      offset-y
      close-on-click
    >
      <template #activator="{ on }">
        <span class="d-flex cursor-pointer mr-4" data-e2e="addicon" v-on="on">
          <tooltip :z-index="99">
            <template #label-content>
              <span :class="{ 'icon-shadow': menu }">
                <icon
                  class="mx-2 my-2 nav-icon"
                  type="more"
                  :size="24"
                  :class="{ 'active-icon': menu }"
                />
              </span>
            </template>
            <template #hover-content> Create / Add </template>
          </tooltip>
        </span>
      </template>
      <v-list>
        <v-list-item>
          <v-list-item-title
            class="font-weight-semi-bold subtitle-1 black--text mt-2 mb-3"
          >
            Create / Add
          </v-list-item-title>
        </v-list-item>
        <v-list-item
          v-for="link in getDropdownLinks"
          :key="link.name"
          :data-e2e="link.name"
          @click="routerRedirect(link.path)"
        >
          <v-list-item-title class="text-body-1 black--text">
            {{ link.name }}
          </v-list-item-title>
        </v-list-item>
      </v-list>
    </v-menu>
    <application
      v-if="
        !clientPanel &&
        role != 'hxtrustid' &&
        getAccess('applications', 'get_all')
      "
    />
    <notification v-if="!clientPanel" />
    <help />
  </div>
</template>

<script>
import Notification from "../components/Notification.vue"
import Help from "../components/Help.vue"
import Icon from "@/components/common/Icon"
import Tooltip from "./common/Tooltip.vue"
import Application from "./Application.vue"
import { mapGetters } from "vuex"
import { getAccess } from "../utils"

export default {
  name: "HeaderNavigation",
  components: {
    Notification,
    Help,
    Icon,
    Tooltip,
    Application,
  },
  data() {
    return {
      dropdownLinks: [
        {
          name: "Data Source",
          path: "DataSources",
          isHidden: !this.getAccess("data_source", "request_new"),
        },
        {
          name: "Destination",
          path: "DestinationConfiguration",
          isHidden: !this.getAccess("destinations", "create_one"),
        },
        {
          name: "Audience",
          path: "SegmentPlayground",
          isHidden: !this.getAccess("audience", "create"),
        },
        {
          name: "Engagement",
          path: "EngagementConfiguration",
          isHidden: !this.getAccess("engagements", "create_one"),
        },
      ],
      appLoadTime: new Date(),
      menu: false,
    }
  },
  computed: {
    ...mapGetters({
      role: "users/getCurrentUserRole",
    }),
    getFormattedTime() {
      let formate = this.$options.filters.Date(this.appLoadTime, "calendar")
      let newFormate = formate.replace(" at", ",")
      return newFormate
    },
    clientPanel() {
      return this.$route.name == "ClientPanel"
    },
    getDropdownLinks() {
      return this.dropdownLinks.filter((x) => !x.isHidden)
    },
  },
  methods: {
    routerRedirect(path) {
      if (
        this.$router.name == path ||
        this.$router.history.current.name == path
      ) {
        this.$root.$emit(`same-route-${path}`)
      } else {
        this.$router.push({
          name: path,
          params: { select: true },
        })
      }
    },
    getAccess: getAccess,
  },
}
</script>

<style lang="scss" scoped>
.v-menu__content {
  margin-left: 126px;
  top: 75px !important;
  .v-list {
    .v-list-item {
      min-height: 32px !important;
    }
  }
}
</style>
