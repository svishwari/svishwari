<template>
  <v-menu :min-width="200" left offset-y close-on-click>
    <template #activator="{ on }">
      <span class="d-flex cursor-pointer" data-e2e="help-dropdown" v-on="on">
        <icon class="mx-2 my-2 nav-icon" type="help" :size="21" />
      </span>
    </template>
    <v-list>
      <v-list-item>
        <v-list-item-title class="font-weight-bold"> Help </v-list-item-title>
      </v-list-item>
      <v-list-item class="v-list-item--link" data-e2e="contactus">
        <a
          href="mailto:ushuxproductidea@deloitte.com"
          class="text-h6 view-all text-decoration-none"
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
  line-height: 22px;
  color: var(--v-black-darken4) !important;
  @extend .cursor-pointer;
}
</style>
