<template>
  <div class="empty-page d-flex justify-center align-center">
    <div class="text-center">
      <v-icon color="primary" x-large>
        <slot name="icon"></slot>
      </v-icon>
      <h3 class="text-h3 my-4">
        <slot name="title"></slot>
      </h3>
      <p class="font-weight-regular mb-4">
        <slot name="subtitle"></slot>
      </p>
      <slot name="button"></slot>
    </div>
  </div>
</template>
<script>
export default {
  name: "EmptyPage",
}
</script>
<style lang="scss" scoped>
.empty-page {
  min-height: 75vh;
  min-width: 100%;

  > div {
    max-width: 38rem;
  }
}
</style>
