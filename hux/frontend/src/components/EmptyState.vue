<template>
  <v-card
    class="text-center pt-16 connection-sources"
    elevation="1"
    tile
    height="340"
    color="aliceBlue"
  >
    <v-icon color="primary" x-large>
      <slot name="icon"></slot>
    </v-icon>
    <v-card-title class="justify-center font-weight-light">
      <slot name="title"></slot>
    </v-card-title>
    <v-card-subtitle>
      <slot name="subtitle"></slot>
    </v-card-subtitle>
  </v-card>
</template>
<script>
export default {
  name: "EmptyState",
}
</script>
<style lang="scss" scoped></style>
