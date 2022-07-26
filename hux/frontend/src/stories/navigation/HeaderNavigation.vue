<template>
  <div class="d-flex align-center">
    <span class="new-b4 top-nav-time mr-1">
      {{ getFormattedTime }}
      <tooltip>
        <template #label-content>
          <span> MST </span>
        </template>
        <template #hover-content> MST </template>
      </tooltip>
    </span>
    <v-icon size="16" class="mr-6 nav-icon"> mdi-refresh </v-icon>
    <v-menu
      v-if="!clientPanel && getDropdownLinks.length > 0"
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
              <span>
                <icon
                  class="nav-icon"
                  type="more"
                  :size="28"
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
          <v-list-item-title class="new-b2 subtitle-1 black--text mt-2 mb-3">
            Create / Add
          </v-list-item-title>
        </v-list-item>
        <v-list-item
          v-for="link in getDropdownLinks"
          :key="link.name"
          :data-e2e="link.name"
        >
          <v-list-item-title class="new-b1 black--text">
            {{ link.name }}
          </v-list-item-title>
        </v-list-item>
      </v-list>
    </v-menu>
    <span class="d-flex cursor-pointer mr-4">
      <tooltip class="tooltip-application" :z-index="99">
        <template #label-content>
          <span>
            <icon class="nav-icon" type="application" :size="28" />
          </span>
        </template>
        <template #hover-content> Application </template>
      </tooltip>
    </span>
    <span class="d-flex cursor-pointer mr-4" v-on="on">
      <tooltip :z-index="99">
        <template #label-content>
          <span>
            <icon class="nav-icon" type="bell-notification" :size="28" />
          </span>
        </template>
        <template #hover-content> Alerts </template>
      </tooltip>
    </span>
    <span class="d-flex cursor-pointer mr-4">
      <tooltip class="tooltip-help" :z-index="99">
        <template #label-content>
          <span>
            <icon class="nav-icon" type="help" :size="28" />
          </span>
        </template>
        <template #hover-content> Help </template>
      </tooltip>
    </span>
  </div>
</template>

<script>
import Icon from "@/components/common/Icon.vue"
import Tooltip from "@/components/common/Tooltip.vue"

export default {
  name: "HeaderNavigation",
  components: {
    Icon,
    Tooltip,
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
    getFormattedTime() {
      return "Today, 12:15 pm"
    },
    clientPanel() {
      return false
    },
    getDropdownLinks() {
      return this.dropdownLinks.filter((x) => !x.isHidden)
    },
  },
  methods: {
    getAccess() {
      return true
    },
  },
}
</script>

<style lang="scss" scoped>
.top-nav-time {
  color: var(--v-primary-lighten7);
}
.v-menu__content {
  margin-left: 126px;
  top: 75px !important;
  .v-list {
    .v-list-item {
      min-height: 32px !important;
    }
  }
}
::v-deep .nav-icon {
  margin: 6px;
}
</style>
