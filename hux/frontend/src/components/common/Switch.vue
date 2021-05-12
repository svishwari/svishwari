<template>
  <v-switch v-model="localValue" inset :label="operandLabel(rule)" @change="onFinalValue"></v-switch>
</template>

<script>
export default {
  name: "switch",
  props: {
      
  },
  computed: {
    localValue: {
      get() {
        return this.value
      },
      set(value) {
        this.$emit("input", value)
      },
    },
  },
  methods: {
    onFinalValue: function (value) {
      this.$emit("onFinalValue", value)
    },
  },
}
</script>

<style lang="scss" scoped></style>
