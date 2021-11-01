<template>
  <v-menu :min-width="192" left offset-y close-on-click>
    <template #activator="{ on }">
      <span
        class="d-flex cursor-pointer mr-4"
        data-e2e="help-dropdown"
        v-on="on"
      >
        <icon class="mx-2 my-2 nav-icon" type="help" :size="24" />
      </span>
    </template>
    <v-list>
      <v-list-item>
        <v-list-item-title class="font-weight-semi-bold text-h6 black--text">
          Help
        </v-list-item-title>
      </v-list-item>
      <v-list-item class="v-list-item--link" data-e2e="about_hux">
        <a href="#" class="text-body-1 black--text text-decoration-none">
          About Hux
        </a>
      </v-list-item>
      <v-list-item class="v-list-item--link" data-e2e="contactus">
        <a
          href="mailto:ushuxproductidea@deloitte.com"
          class="text-body-1 black--text view-all text-decoration-none"
        >
          Contact Us
        </a>
      </v-list-item>
    </v-list>
  </v-menu>
</template>

<script>
import Icon from "@/components/common/Icon"
export default {
  name: "Help",
  components: {
    Icon,
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
  @extend .cursor-pointer;
}
</style>
