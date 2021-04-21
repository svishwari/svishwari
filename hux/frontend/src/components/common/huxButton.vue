<template>
  <div>
    <v-btn :disabled="isDisabled" :outlined="isOutlined" :tile="isTile" :color="variant"  class="ma-2" :class="buttonSize">
      <v-icon v-show="iconPosition == 'left'" dark class="mr-1"> {{ icon }} </v-icon>
      {{ ButtonText }}
      <v-icon v-show="iconPosition == 'right'" dark class="mr-1">  {{ icon }} </v-icon>
    </v-btn>
  </div>
</template>

<script>
export default {
  name: "huxButton",
  props: {
    ButtonText: {
      type: String,
      required: false,
      default: "Added",
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
      type: Boolean
    },
    isDisabled: {
      type: Boolean
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
  },
  computed: {
    buttonSize: function () {
      return 'v-size--' + this.size
    }
  },
}
</script>
