<template>
  <v-footer
    class="app-footer-wrap d-flex justify-space-between align-center shadow"
    app
    paddless
    fixed
    inset
    color="background"
  >
    <div class="footer--left">
      <slot name="left"></slot>
    </div>
    <div class="footer--right">
      <slot name="right"></slot>
    </div>
  </v-footer>
</template>

<script>
export default {
  name: "hux-footer",
}
</script>
<style lang="scss" scoped>
.app-footer-wrap {
  padding: 1rem 10rem;
}
</style>
