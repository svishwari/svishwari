<template>
  <v-btn
    :loading="loading"
    :disabled="isDisabled"
    :outlined="isOutlined"
    :tile="isTile"
    :color="variant"
    :class="[buttonSize, { 'box-shadow-25': boxShadow }]"
    :width="width"
    :height="height"
    :icon="iconType"
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
import Icon from "../common/Icon.vue"
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
    isOutlined: {
      type: Boolean,
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
      default: 14,
    },
    iconClass: {
      type: String,
      required: false,
      default: "ml-2 mr-2"
    }
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
