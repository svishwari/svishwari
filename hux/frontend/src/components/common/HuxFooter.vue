<template>
  <v-footer class="page-footer" app paddless fixed height="80" inset>
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
  padding: 20px 32px;
  border-color: var(--v-black-lighten3) !important;
  background-color: var(--v-primary-lighten1) !important;
  box-sizing: inherit;
  @extend .border-top;
  @extend .box-shadow-none;

  .page-footer-container {
    width: 100%;
    max-width: 1220px;
    margin: 0 auto;
  }
}
</style>
