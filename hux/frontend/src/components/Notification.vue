<template>
  <v-badge content="2" value="2" color="red" overlap class="notification-badge">
    <v-btn icon class="icon-btn">
      <v-icon class="mdi-bell-outline"> mdi-bell-outline </v-icon>
    </v-btn>
  </v-badge>
</template>

<script>
export default {
  name: "Notification",
};
</script>
<style lang="scss" scoped>
.notification-badge {
  .icon-btn {
    box-shadow: 0px 1px 5px rgb(0 0 0 / 25%);
    i.v-icon.notranslate.mdi {
      color: #005587 !important;
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
