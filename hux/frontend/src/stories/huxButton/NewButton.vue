<template>
  <v-hover v-slot="{ hover }">
    <v-btn
      class="px-6"
      :outlined="variant == 'secondary'"
      :disabled="disabled"
      :style="{
        color:
          'var(--v-' +
          (variant == 'secondary'
            ? hover
              ? getHoverColor()
              : getColor()
            : 'white-base') +
          ') !important',
        backgroundColor:
          'var(--v-' +
          (variant == 'secondary'
            ? 'white-base'
            : hover
            ? getHoverColor()
            : getColor()) +
          ') !important',
      }"
      @click="onClick"
    >
      <div class="button-content text-b3">
        <icon
          v-if="icon"
          :type="icon"
          size="15"
          :color="getColor()"
          outline
          border-color="white-base"
          class="mr-2"
        />
        <slot name="default" />
      </div>
    </v-btn>
  </v-hover>
</template>

<script>
import Icon from "../icons/Icon2.vue"

export default {
  name: "NewButton",
  components: { Icon },
  props: {
    icon: {
      type: String,
      required: false,
      default: null,
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
    variant: {
      type: String,
      required: false,
      default: "primary",
    },
  },
  methods: {
    onClick: function () {
      this.$emit("click")
    },
    getColor() {
      if (this.disabled) return "black-lighten5"
      if (this.danger) return "error-lighten1"
      return "primary-lighten7"
    },
    getHoverColor() {
      if (!this.disabled && !this.danger) return "primary-base"
      return this.getColor()
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
