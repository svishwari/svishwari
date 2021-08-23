<template>
  <v-menu :min-width="200" left offset-y close-on-click>
    <template #activator="{ on }">
      <span class="d-flex cursor-pointer" v-on="on">
        <v-btn class="mx-2 box-shadow-25" color="white" fab x-small>
          <v-icon color="primary"> mdi-help </v-icon>
        </v-btn>
      </span>
    </template>
    <v-list>
      <v-list-item>
        <v-list-item-title class="font-weight-bold">
          Help
        </v-list-item-title>
      </v-list-item>
      <v-list-item class="v-list-item--link">
        <router-link
          :to="{
            name: 'Overview',
          }"
          class="text-h6 view-all text-decoration-none"
        >
          Contact Us
        </router-link>
      </v-list-item>
    </v-list>
  </v-menu>
</template>

<script>

export default {
  name: "Help",
  data() {
    return {
      path: "Overview"
    }
  },
  methods: {
    routerRedirect(path) {
      this.$router.push({ name: path, query: { select: true } })
    },
  },
}

</script>

<style lang="scss" scoped>
.v-menu__content {
  top: 64px !important;
  .v-list {
    .v-list-item {
      min-height: 40px !important;
    }
  }
}
.view-all {
  font-family: Open Sans;
  font-style: normal;
  font-weight: normal;
  font-size: 14px;
  line-height: 22px;
  color: var(--v-neroblack-base) !important;
  cursor: pointer;
}
</style>
