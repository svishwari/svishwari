<template>
  <v-btn
    :text="textOnly"
    class="px-6"
    :outlined="outlined"
    :disabled="disabled"
    @click="onClick"
    :style="{
      color: `${getTxtColor(
        disabled ? 'black-lighten5' : danger ? 'error-lighten1' : color
      )} !important`,
      backgroundColor: `${getBtnColor(
        disabled ? 'black-lighten5' : danger ? 'error-lighten1' : color
      )} !important`,
    }"
  >
    <div class="button-content text-button">
      <icon
        v-if="icon"
        :type="icon"
        size="15"
        :color="iconColor"
        class="mr-2"
      />
      <slot name="default" />
    </div>
  </v-btn>
</template>

<script>
import Icon from "../icons/Icon2.vue"

export default {
  name: "NewButton",
  components: { Icon },
  props: {
    textOnly: {
      type: Boolean,
      required: false,
      default: false,
    },
    icon: {
      type: String,
      required: false,
      default: null,
    },
    color: {
      type: String,
      required: false,
      default: "secondary",
    },
    iconColor: {
      type: String,
      required: false,
      default: "primary",
    },
    outlined: {
      type: Boolean,
      required: false,
      default: false,
    },
    disabled: {
      type: Boolean,
      required: false,
      default: false,
    },
    danger: {
      type: Boolean,
      required: false,
      default: false,
    },
  },
  methods: {
    onClick: function () {
      this.$emit("click")
    },
    getTxtColor(color) {
      if (this.outlined || this.textOnly) return `var(--v-${color})`
      else return `var(--v-white-base)`
    },
    getBtnColor(color) {
      if (this.outlined || this.textOnly) return `var(--v-white-base)`
      else return `var(--v-${color})`
    },
  },
}
</script>

<style lang="scss" scoped>
.button-content {
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>
