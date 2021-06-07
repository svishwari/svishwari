<template>
  <div class="form-steps">
    <slot name="default" />
  </div>
</template>

<script>
export default {
  name: "FormSteps",
}
</script>

<style lang="scss">
.form-steps {
  .form-step:last-child {
    .form-step__content {
      border-left: 0;
    }
  }
}
</style>
