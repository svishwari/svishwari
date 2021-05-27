<template>
  <div class="d-flex navbar-menu align-center">
    <v-btn small icon class="icon-btn">
      <v-icon size="22" class="mdi-plus">mdi-plus</v-icon>
    </v-btn>
    <Notification></Notification>
    <v-btn small icon class="icon-btn">
      <v-icon size="20" class="mdi-help">mdi-help</v-icon>
    </v-btn>
    <v-divider vertical color="lightGrey"></v-divider>
    <UserAvatar></UserAvatar>
  </div>
</template>

<script>
import Notification from "@/components/Notification"
import UserAvatar from "@/components/UserAvatar"

export default {
  name: "NavBarMenu",
  components: { Notification, UserAvatar },
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
      border: 1px solid #d0d0ce;
      margin-right: 9px;
      margin-left: 9px;
    }
  }
}
</style>
