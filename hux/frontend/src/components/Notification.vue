<template>
  <v-badge
    bottom
    color="red"
    content="2"
    value="2"
    offset-x="20"
    offset-y="30"
    class="notification-badge font-weight-semi-bold"
  >
    <v-btn small icon class="icon-btn">
      <v-icon size="20" class="mdi-bell-outline"> mdi-bell-outline </v-icon>
    </v-btn>
  </v-badge>
</template>

<script>
export default {
  name: "Notification",
}
</script>
<style lang="scss" scoped>
.notification-badge {
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
}
</style>
