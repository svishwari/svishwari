<template>
  <v-badge content="2" value="2" color="red" overlap>
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
<style lang="scss">
.v-application--is-ltr .v-badge__badge {
  inset: auto auto calc(100% - 32px) calc(100% - 32px) !important;
}
</style>
