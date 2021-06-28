<template>
  <v-menu v-model="menu" offset-y close-on-click>
    <template #activator="{ on }">
      <span v-on="on" class="d-flex cursor-pointer mr-6">
        <v-btn class="mx-2" fab small color="white">
          <v-icon color="secondary"> mdi-plus </v-icon>
        </v-btn>
      </span>
    </template>
    <v-list>
      <v-list-item>
        <v-list-item-title class="add"> Add </v-list-item-title>
      </v-list-item>
      <v-list-item v-for="link in dropdownLinks" :key="link">
        <v-list-item-title class="text-h6 neroBlack--text">
          <router-link
            :to="{
              name: link.path,
            }"
            class="text-decoration-none"
            append
            >{{ link.name }}
          </router-link>
        </v-list-item-title>
      </v-list-item>
    </v-list>
  </v-menu>
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
}
</script>

<style lang="scss">
.add {
  font-style: normal;
  font-weight: 600;
  font-size: 14px;
  line-height: 19px;
  margin-bottom: 10px;
}
</style>
