<template>
  <v-footer
    class="app-footer-wrap d-flex justify-space-between align-center"
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
  box-shadow: 0px -0.5px 5px 1px rgba(0, 0, 0, 0.15) !important;
}
</style>
