<template>
  <v-card class="empty-card text-center py-16" outlined>
    <v-icon color="#00A3E0" x-large>
      <slot name="icon"></slot>
    </v-icon>
    <v-card-title class="justify-center text-h4 font-weight-light mb-4">
      <slot name="title"></slot>
    </v-card-title>
    <v-card-subtitle class="body-1 black--text">
      <slot name="subtitle"></slot>
    </v-card-subtitle>
  </v-card>
</template>
<script>
export default {
  name: "EmptyState",
}
</script>
<style lang="scss" scoped>
.empty-card {
  border: 1px solid var(--v-zircon-base);
  background: var(--v-white-base);
}
</style>
