<template>
  <div class="ma-2">
    <slot name="default">
      <div class="pl-2">Header</div>
      <v-card class="small-list-card">Content</v-card>
    </slot>
  </div>
</template>

<script>
export default {
  name: "SmallListItem",
}
</script>

<style lang="scss" scoped>
.small-list-card {
  display: inline-block;
  padding: 12px;
}
</style>
