<template>
  <div class="d-flex navbar-menu align-center">
    <header-navigation />
    <v-divider vertical color="lightGrey" />
    <user-avatar />
  </div>
</template>

<script>
import UserAvatar from "@/components/UserAvatar"
import HeaderNavigation from "@/components/HeaderNavigation"

export default {
  name: "NavBarMenu",
  components: { UserAvatar, HeaderNavigation },
}
</script>

<style lang="scss" scoped>
.navbar-menu {
  .v-application--wrap {
    button {
      margin: 5px;
    }
  }
  .icon-btn {
    box-shadow: 0px 1px 5px rgb(0 0 0 / 25%);
    i.v-icon.notranslate.mdi {
      color: var(--v-primary-base);
    }
    &.v-btn {
      &.v-btn--icon {
        &.v-btn--round {
          margin-right: 9px;
          margin-left: 9px;
        }
      }
    }
  }
  .v-divider {
    &.v-divider--vertical {
      border: 0;
      border-left: 1px solid var(--v-lightGrey-base);
      margin-right: 9px;
      margin-left: 9px;
    }
  }
}
</style>
