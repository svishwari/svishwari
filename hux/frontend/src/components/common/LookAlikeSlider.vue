<template>
  <transition>
    <v-slider
      v-model="localValue"
      :tick-labels="ticksLabels"
      :max="max"
      :min="min"
      :step="step"
      ticks="always"
      class="hux-lookalike-slider"
      @end="onFinalValue"
    />
  </transition>
</template>

<script>
export default {
  name: "look-alike-slider",
  props: {
    value: {
      type: Number,
      required: true,
    },
    min: {
      type: Number,
      required: false,
      default: 1,
    },
    max: {
      type: Number,
      required: false,
      default: 10,
    },
    step: {
      type: Number,
      required: false,
      default: 1,
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
    ticksLabels() {
      return Array.from({ length: this.max }, (_, i) => `${i + 1}%`)
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
.hux-lookalike-slider {
  ::v-deep .v-input__control {
    .v-input__slot {
      .v-slider--horizontal {
        margin: 0px;
      }
      .v-slider__track-container {
        height: 6px;
      }
      .v-slider__track-container {
        .v-slider__track-fill {
          background-color: rgba(0, 171, 171, 0.55) !important;
          border-radius: 10px 0 0 10px;
        }
        .v-slider__track-background {
          background-color: rgba(0, 171, 171, 0.55) !important;
          border-radius: 0 10px 10px 0;
        }
      }
      .v-slider__ticks-container {
        .v-slider__tick {
          background-color: rgba(0, 171, 171, 0.55) !important;
          width: 0 !important;
        }
      }
      .v-slider__thumb {
        width: 16px;
        height: 16px;
        background-color: var(--v-white-base) !important;
        border: 1px solid rgba(0, 171, 171, 0.55);
        box-sizing: border-box;
        border-color: rgba(0, 171, 171, 0.55) !important;
        @extend .box-shadow-15;
      }
    }
  }
}
</style>
