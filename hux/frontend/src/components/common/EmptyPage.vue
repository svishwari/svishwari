<template>
  <div class="empty-page d-flex justify-center align-center">
    <div class="text-center">
      <slot name="icon">
        <icon
          :type="type"
          :size="size"
        />
      </slot>
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
import Icon from "../../components/common/Icon"
export default {
  name: "EmptyPage",
  components: { 
    Icon,
  },
  props: {
    type: {
      type: String,
      required: false,
    },
    size: {
      type: String,
      required: false,
    },
  },
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
