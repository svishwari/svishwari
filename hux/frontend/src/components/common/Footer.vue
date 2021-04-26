<template>
  <v-footer
    class="app-footer-wrap d-flex justify-space-between align-center"
    app
    paddless
    fixed
    height="80"
    inset
    color="background"
    elevation="5"
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
  name: "footer",
}
</script>
<style lang="scss" scoped>
.app-footer-wrap {
  padding: 14px 169px;
}
</style>
