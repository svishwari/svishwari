<template>
  <div>
    <slot name="header" />
    <div class="container" :style="{ 'max-width': maxWidth, padding: padding }">
      <slot />
    </div>
    <slot name="footer" />
  </div>
</template>

<script>
export default {
  name: "Page",

  props: {
    maxWidth: {
      type: String,
      required: false,
    },
    padding: {
      type: String,
      required: false,
    },
  },
}
</script>

<style lang="scss" scoped>
.container {
  max-width: 1220px;
  padding: 30px;
}
</style>
