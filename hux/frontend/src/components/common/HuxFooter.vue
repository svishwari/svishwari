<template>
  <v-footer
    class="page-footer shadow"
    app
    paddless
    fixed
    height="80"
    inset
    color="primary lighten-1"
  >
    <div
      class="page-footer-container d-flex justify-space-between align-center"
      :style="{ 'max-width': maxWidth }"
    >
      <div class="footer--left">
        <slot name="left"></slot>
      </div>
      <div class="footer--right">
        <slot name="right"></slot>
      </div>
    </div>
  </v-footer>
</template>

<script>
export default {
  name: "HuxFooter",

  props: {
    maxWidth: {
      type: String,
      required: false,
    },
  },
}
</script>

<style lang="scss" scoped>
.page-footer {
  padding: 20px 60px;

  .page-footer-container {
    width: 100%;
    max-width: 1220px;
    margin: 0 auto;
  }
}
</style>
