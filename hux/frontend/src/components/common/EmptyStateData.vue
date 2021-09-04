<template>
  <v-card class="empty-card text-center py-16" outlined>
    <v-icon color="primary lighten-8" x-large>
      <slot name="icon"></slot>
    </v-icon>
    <v-card-title
      class="justify-center neroBlack--text text-h4 font-weight-light mb-4"
    >
      <slot name="title"></slot>
    </v-card-title>
    <v-card-subtitle class="body-1 neroBlack--text">
      <slot name="subtitle"></slot>
    </v-card-subtitle>
  </v-card>
</template>
<script>
export default {
  name: "EmptyStateData",
}
</script>
<style lang="scss" scoped>
.empty-card {
  border: 1px solid var(--v-zircon-base);
  background: var(--v-white-base);
}
</style>
