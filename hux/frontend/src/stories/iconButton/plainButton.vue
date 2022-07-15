<template>
  <v-btn
    text
    plain
    :ripple="false"
    class="primary--text new-b3"
    data-e2e="drawerToggle"
    @click.native="onClick()"
  >
    <icon
      v-if="raised"
      type="Add"
      size="17"
      color="primary-lighten7"
      class="mr-2"
      @click.native="onClick()"
    />
    <icon
      :type="icon"
      :size="iconSize"
      color="primary"
      :class="{
        'mr-2 hoverIcon': true,
        'box-shadow-15-4': raised,
        'selected-icon': !raised,
      }"
      :style="{ 'border-radius': '50%' }"
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
      default: "primary",
    },
    raised: {
      type: Boolean,
      required: false,
      default: true,
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
  &:hover {
    box-shadow: none !important;
  }
}
.selected-icon {
  background: var(--v-black-lighten1);
  border-radius: 2px;
}
</style>
