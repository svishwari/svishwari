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
    @click="loader = 'loading'"
  >
    <v-icon v-show="iconPosition == 'left'" dark class="mr-1">
      {{ icon }}
    </v-icon>
    {{ ButtonText }}
    <v-icon v-show="iconPosition == 'right'" dark class="mr-1">
      {{ icon }}
    </v-icon>
  </v-btn>
</template>

<script>
export default {
  name: "huxButton",
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
    ButtonText: {
      type: String,
      required: false,
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
}
</script>
