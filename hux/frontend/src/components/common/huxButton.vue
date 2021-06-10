<template>
  <v-btn
    :loading="loading"
    :disabled="isDisabled"
    :outlined="isOutlined"
    :tile="isTile"
    :color="variant"
    :class="buttonSize"
    :width="width"
    :height="height"
    :icon="iconType"
    @click="onClick"
  >
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
export default {
  name: "HuxButton",
  data() {
    return {
      loader: null,
      loading: false,
    }
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
      default: null,
    },
    iconType: {
      type: Boolean,
      required: false,
      default: null,
    },
  },
  computed: {
    buttonSize: function () {
      return "v-size--" + this.size
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
