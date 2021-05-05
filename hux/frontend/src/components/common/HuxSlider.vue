<template>
  <v-range-slider
    :max="max"
    :min="min"
    :step="step"
    thumb-label="always"
    v-model="localValue"
    class="huxSlider"
    @end="onFinalValue"
  ></v-range-slider>
</template>

<script>
export default {
  name: "huxSlider",
  props: {
    value: {
      type: Array,
      required: true,
    },
    min: {
      type: Number,
      required: true,
    },
    max: {
      type: Number,
      required: true,
    },
    step: {
      required: true,
    },
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

<style lang="scss" scoped>
.huxSlider {
  ::v-deep .v-input__control {
    .v-input__slot {
      .v-slider__track-container {
        height: 4px;
      }
      .lighten-3 {
        background-color: rgba(157, 212, 207, 0.25) !important;
      }
      .theme--light {
        .v-slider__track-fill {
          background-color: #00abab !important;
        }
      }
      .v-slider__thumb {
        width: 16px;
        height: 16px;
        background-color: #ffffff !important;
        border: 1px solid #00abab;
        box-sizing: border-box;
        box-shadow: 0px 1px 5px rgb(0 0 0 / 15%);
        border-radius: 100px;
        border-color: #00abab !important;
      }
      .v-slider__thumb-label {
        transform: translateY(35px) translateX(-50%) rotate(45deg) !important;
        background-color: inherit !important;
        color: #4f4f4f;
        border: none !important;
        font-size: 12px;
        line-height: 16px;
      }
    }
  }
}
</style>
