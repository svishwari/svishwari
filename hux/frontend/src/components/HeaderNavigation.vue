<template>
  <div class="d-flex align-center">
    <span class="text--body-2 black--text text--lighten-4 mr-2">
      Today,
      {{ appLoadTime | Date("HH:mm A zzz") }}
    </span>
    <v-icon size="16" class="mr-2 nav-icon" @click="$router.go()">
      mdi-refresh
    </v-icon>
    <v-menu :min-width="200" left offset-y close-on-click>
      <template #activator="{ on }">
        <span class="d-flex cursor-pointer" data-e2e="addicon" v-on="on">
          <icon class="mx-2 my-2 nav-icon" type="more" :size="21" />
        </span>
      </template>
      <v-list>
        <v-list-item>
          <v-list-item-title
            class="
              font-weight-semi-bold
              text-h6
              black--text
              text--lighten-4
              mb-1
            "
          >
            Add
          </v-list-item-title>
        </v-list-item>
        <v-list-item
          v-for="link in dropdownLinks"
          :key="link.name"
          @click="routerRedirect(link.path)"
        >
          <v-list-item-title class="text-body-1 black--text text--lighten-4">
            {{ link.name }}
          </v-list-item-title>
        </v-list-item>
      </v-list>
    </v-menu>
    <notification />
    <help />
  </div>
</template>

<script>
import Notification from "../components/Notification.vue"
import Help from "../components/Help.vue"
import Icon from "@/components/common/Icon"
export default {
  name: "HeaderNavigation",
  components: {
    Notification,
    Help,
    Icon,
  },
  data() {
    return {
      dropdownLinks: [
        { name: "Data Source", path: "Connections" },
        { name: "Destination", path: "DestinationConfiguration" },
        { name: "Audience", path: "AudienceConfiguration" },
        { name: "Engagement", path: "EngagementConfiguration" },
      ],
      appLoadTime: new Date(),
    }
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
  },
}
</script>

<style lang="scss" scoped>
.v-menu__content {
  top: 64px !important;
  .v-list {
    .v-list-item {
      min-height: 32px !important;
    }
  }
}
</style>
