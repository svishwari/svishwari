<template>
  <v-btn
    text
    plain
    :ripple="false"
    :class="['new-b2 icon-button', variant]"
    data-e2e="drawerToggle"
    :disabled="isDisabled"
    @click.native="onClick()"
  >
    <icon
      v-if="raised"
      type="Add"
      :size="iconSize"
      color="primary-lighten7"
      class="mr-2"
      @click.native="onClick()"
    />
    <icon
      :type="icon"
      :size="iconSize"
      :color="iconColor"
      :border-color="iconColor"
      outline
      :class="{
        'mr-2 hoverIcon': true,
        'box-shadow-15-4': raised,
        'selected-icon': !raised,
      }"
      @click.native="onClick()"
    />

    <slot name="default"></slot>
  </v-btn>
</template>

<script>
import Icon from "../icons/Icon2.vue"
export default {
  name: "IconButton",
  components: {
    Icon,
  },
  props: {
    variant: {
      type: String,
      required: false,
      default: "default",
    },
    icon: {
      type: String,
      required: false,
      default: null,
    },
    isDisabled: {
      type: Boolean,
      required: false,
      default: false,
    },
    iconColor: {
      type: String,
      required: false,
      default: "primary-lighten7",
    },
    raised: {
      type: Boolean,
      required: false,
      default: true,
    },
    iconSize: {
      type: Number,
      required: false,
      default: 24,
    },
  },
  data() {
    return {
      selected: false,
    }
  },
  methods: {
    onClick: function () {
      this.selected = !this.selected
      this.$emit("click")
    },
  },
}
</script>
<style lang="scss" scoped>
.hoverIcon {
  &:active {
    box-shadow: none !important;
  }
}
.selected-icon {
  background: var(--v-black-lighten1);
  border-radius: 2px;
}
::v-deep.icon-button {
  .v-btn__content {
    color: var(--v-primary-lighten7) !important;
  }
  &.danger {
    .v-btn__content {
      svg {
        fill: var(--v-error-lighten1) !important;
        border-color: var(--v-error-lighten1) !important;
        &:hover,
        &:active {
          border: 0px !important;
        }
        &:active {
          background-color: #fdf4f4 !important;
        }
      }
      color: var(--v-error-lighten1) !important;
    }
  }
  &.v-btn--disabled {
    .v-btn__content {
      svg {
        fill: var(--v-black-lighten5) !important;
        border-color: var(--v-black-lighten5) !important;
      }
      color: var(--v-black-lighten6) !important;
    }
  }
}
</style>
