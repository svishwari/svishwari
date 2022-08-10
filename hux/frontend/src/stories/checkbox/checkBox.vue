<template>
  <v-checkbox :disabled="isDisabled" @click="onClick()" />
</template>

<script>
export default {
  name: "CheckBox",
  components: {},
  props: {
    isDisabled: {
      type: Boolean,
      required: false,
      default: false,
    },
  },
  data() {
    return {}
  },
  computed: {},
  methods: {
    onClick: function () {
      this.$emit("click")
    },
  },
}
</script>
<style lang="scss" scoped>
::v-deep.v-input--is-disabled.v-input--checkbox {
  .v-input__control {
    color: var(--v-black-lighten5);
  }
}
</style>
