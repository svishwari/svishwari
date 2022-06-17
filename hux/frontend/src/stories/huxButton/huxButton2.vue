<template>
  <v-btn
    :loading="loading"
    :disabled="isDisabled"
    :outlined="isOutlined"
    :tile="isTile"
    :class="[
      sidePadding,
      buttonSize,
      { 'box-shadow-15-4': boxShadow },
      'text-button',
      variant,
    ]"
    :style="styleObject"
    :color="color"
    :width="width"
    :height="height"
    :icon="iconType"
    :ripple="false"
    @click="onClick"
  >
    <icon
      v-if="isCustomIcon"
      :class="iconClass"
      :color="iconColor"
      :variant="iconVariant"
      :type="icon"
      :size="iconSize"
    />
    <v-icon v-show="iconPosition == 'left'" dark class="mr-1">
      {{ icon }}
    </v-icon>
    <v-spacer> </v-spacer>

    <!-- {{ ButtonText }} -->
    <slot name="default"></slot>

    <v-spacer> </v-spacer>
    <v-icon v-show="iconPosition == 'right'" dark class="mr-1">
      {{ icon }}
    </v-icon>
  </v-btn>
</template>

<script>
import Icon from "@/components/common/Icon.vue"
export default {
  name: "HuxButton",
  components: {
    Icon,
  },
  props: {
    enableLoading: {
      type: Boolean,
      required: false,
      default: false,
    },
    icon: {
      type: String,
      required: false,
      default: null,
    },
    iconPosition: {
      type: String,
      required: false,
      default: null,
    },
    variant: {
      type: String,
      required: false,
      default: "primary",
    },
    isDisabled: {
      type: Boolean,
      default: false,
    },
    isTile: {
      type: Boolean,
      required: false,
      default: false,
    },
    size: {
      type: String,
      required: false,
      default: null,
    },
    width: {
      type: String,
      required: false,
      default: null,
    },
    height: {
      type: String,
      required: false,
      default: "40",
    },
    iconType: {
      type: Boolean,
      required: false,
      default: null,
    },
    boxShadow: {
      type: Boolean,
      required: false,
      default: true,
    },
    isCustomIcon: {
      type: Boolean,
      required: false,
      default: false,
    },
    iconColor: {
      type: String,
      required: false,
      default: "primary",
    },
    iconVariant: {
      type: String,
      required: false,
      default: "base",
    },
    iconSize: {
      type: Number,
      required: false,
      default: 15,
    },
    iconClass: {
      type: String,
      required: false,
      default: "mx-2",
    },
    sidePadding: {
      type: String,
      required: false,
      default: "px-6",
    },
  },
  data() {
    return {
      loader: null,
      loading: false,
    }
  },
  computed: {
    buttonSize: function () {
      return "v-size--" + this.size
    },
    buttonTextColor: function () {
      return this.ButtonTextColor
    },
    styleObject: function () {
      if (this.variant == "danger") {
        return {
          "--color": this.variant == "secondary" ? "error" : "white",
          "--color-hover": "error",
        }
      } else {
        return {
          "--color": this.variant == "secondary" ? "primary darken-1" : "white",
          "--color-hover": "--v-primary-base",
        }
      }
    },
    color() {
      return this.variant == "danger" ? "error" : "primary darken-1"
    },
    isOutlined() {
      return this.variant == "secondary"
    },
  },
  watch: {
    loader() {
      if (this.enableLoading) {
        const l = this.loader
        this[l] = !this[l]
        setTimeout(() => (this[l] = false), 3000)
        this.loader = null
      }
    },
  },
  methods: {
    onClick: function () {
      this.$emit("click")
      this.loader = "loading"
    },
  },
}
</script>
<style lang="scss" scoped>
$btn-active-opacity: 0 !important;
$btn-hover-opacity: 0 !important;

::v-deep .tooltip-subheading {
  line-height: 20px !important;
}

::v-deep.v-btn.v-btn--disabled.v-btn--has-bg {
  background-color: var(--v-black-lighten5) !important;
  color: var(--v-white-base) !important;
}

::v-deep.theme--light.v-btn.v-btn--disabled .v-icon {
  color: var(--v-white-base) !important;
}

.v-application .white {
  border: solid 1px var(--v-black-lighten1) !important;
}

button.v-btn.text-button {
  &.primary {
    &:hover {
      @extend .box-shadow-15-8;
      background-color: var(--v-primary-base) !important;
      border-color: var(--v-primary-base) !important;
      ::v-deep.v-btn__content {
        color: var(--color) !important;
      }
    }
    &:active {
      @extend .box-shadow-none;
      background-color: var(--v-primary-base) !important;
      border-color: var(--v-primary-base) !important;
      ::v-deep.v-btn__content {
        color: var(--color) !important;
      }
    }
  }
  &.secondary {
    background-color: var(--v-white-base) !important;
    border-color: var(--v-primary-base) !important;
    &:hover {
      @extend .box-shadow-15-8;
      background-color: var(--v-white-base) !important;
      border-color: var(--v-primary-base) !important;
      ::v-deep.v-btn__content {
        color: var(--v-primary-base) !important;
      }
    }
    &:active {
      @extend .box-shadow-none;
      background-color: var(--v-primary-base) !important;
      border-color: var(--v-primary-base) !important;
      ::v-deep.v-btn__content {
        color: var(--v-white-base) !important;
      }
    }
    &.v-btn--disabled {
      border: 0px !important;
      background-color: var(--v-black-lighten5) !important;
      color: var(--v-white-base) !important;
    }
  }
  &.danger {
    &:hover {
      @extend .box-shadow-15-8;
      background-color: var(--v-white-base) !important;
      border-color: transparent !important;
      ::v-deep.v-btn__content {
        color: var(--v-error-lighten1) !important;
      }
    }
    &:active {
      @extend .box-shadow-none;
      background-color: var(--v-white-base) !important;
      border: 0.5px solid var(--v-error-lighten1) !important;
      ::v-deep.v-btn__content {
        color: var(--v-error-lighten1) !important;
      }
    }
  }
}
</style>
