<template>
  <span class="header-menu">
    <v-menu :min-width="200" left offset-y close-on-click>
      <template #activator="{ on }">
        <span v-on="on" class="d-flex cursor-pointer mr-6">
          <v-btn class="mx-2 box-shadow-25" fab small color="white">
            <v-icon color="secondary"> mdi-plus </v-icon>
          </v-btn>
        </span>
      </template>
      <v-list>
        <v-list-item>
          <v-list-item-title class="font-weight-bold"> Add </v-list-item-title>
        </v-list-item>
        <v-list-item
          @click="routerRedirection(link.path)"
          v-for="link in dropdownLinks"
          :key="link.name"
        >
          <v-list-item-title class="text-h6 neroBlack--text">
            {{ link.name }}
          </v-list-item-title>
        </v-list-item>
      </v-list>
    </v-menu>
  </span>
</template>

<script>
export default {
  name: "HeaderNavigation",
  data() {
    return {
      dropdownLinks: [
        { name: "Data Source", path: "DataSourceConfiguration" },
        { name: "Destination", path: "DestinationConfiguration" },
        { name: "Audience", path: "AudienceConfiguration" },
        { name: "Engagement", path: "EngagementConfiguration" },
      ],
    }
  },
  methods: {
    routerRedirection(path) {
      this.$router.push({ name: path, query: { select: true } })
    },
  },
}
</script>

<style lang="scss" scoped>
.header-menu {
  margin-right: -32px !important;
  .v-menu__content {
    top: 64px;
  }
}

.v-list {
  .v-list-item {
    min-height: 40px !important;
  }
}
</style>
