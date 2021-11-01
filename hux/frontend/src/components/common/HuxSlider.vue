<template>
  <transition>
    <v-range-slider
      v-if="isRangeSlider"
      v-model="localValue"
      class="hux-range-slider"
      :max="max"
      :min="min"
      :step="step"
      thumb-label="always"
      @end="onFinalValue"
    ></v-range-slider>
    <v-slider
      v-else
      v-model="currentValue"
      class="hux-score-slider"
      always-dirty
      :color="currentColor"
      :readonly="readOnly"
      :track-color="currentColor"
      @end="onFinalValue"
    >
      <template #append>
        <span
          class="slider-value-display black--text text-subtitle-1"
          v-text="currentValue + '%'"
        ></span>
      </template>
    </v-slider>
  </transition>
</template>

<script>
import colors from "../../plugins/colors"

export default {
  name: "HuxSlider",
  props: {
    value: {
      type: [Number, Array],
      required: true,
    },
    min: {
      type: Number,
      required: false,
    },
    max: {
      type: Number,
      required: false,
    },
    step: {
      required: false,
    },
    readOnly: {
      type: Boolean,
      required: false,
      default: true,
    },
    isRangeSlider: {
      type: Boolean,
      required: true,
      default: false,
    },
  },
  data() {
    return {
      currentValue: this.isRangeSlider
        ? this.value
        : parseInt(this.$options.filters.Percentage(this.value).slice(0, -1)),
      colorCombination: colors.gradientSliderColors,
    }
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
    currentColor: function () {
      if (this.currentValue < 8) return this.colorCombination[0]
      if (this.currentValue < 16) return this.colorCombination[1]
      if (this.currentValue < 24) return this.colorCombination[2]
      if (this.currentValue < 32) return this.colorCombination[3]
      if (this.currentValue < 40) return this.colorCombination[4]
      if (this.currentValue < 48) return this.colorCombination[5]
      if (this.currentValue < 56) return this.colorCombination[6]
      if (this.currentValue < 64) return this.colorCombination[7]
      if (this.currentValue < 72) return this.colorCombination[8]
      if (this.currentValue < 80) return this.colorCombination[9]
      if (this.currentValue < 88) return this.colorCombination[10]
      if (this.currentValue < 96) return this.colorCombination[11]
      return this.colorCombination[11]
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
.hux-range-slider {
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
          background-color: rgba(0, 171, 171, 0.55) !important;
        }
      }
      .v-slider__thumb {
        width: 16px;
        height: 16px;
        background-color: var(--v-white-base) !important;
        border: 1px solid rgba(0, 171, 171, 0.55);
        box-sizing: border-box;
        box-shadow: 0px 1px 5px rgb(0 0 0 / 15%);
        border-radius: 100px;
        border-color: rgba(0, 171, 171, 0.55) !important;
      }
      .v-slider__thumb-label {
        transform: translateY(35px) translateX(-50%) rotate(45deg) !important;
        background-color: inherit !important;
        color: var(--v-black-darken1);
        border: none !important;
      }
    }
  }
}
.hux-score-slider {
  ::v-deep .v-input__control {
    .v-input__slot {
      margin: 0;
    }
    .v-messages {
      display: none;
    }
  }
  margin-left: 10px;
  margin-right: 10px;

  .slider-value-display {
    height: 16px;
    margin-top: -3px;
    margin-left: 3px;
  }

  ::v-deep .v-slider__thumb {
    height: 16px;
    width: 16px;
    @extend .box-shadow-15;
    -webkit-appearance: none;
    appearance: none;

    &:before {
      left: -10px;
      top: -10px;
    }
  }

  ::v-deep .v-slider--horizontal {
    margin-left: 0px;
    margin: 0;
    min-height: 28px;

    .v-slider__track-container {
      width: 101%;
      height: 6px;
      left: -6px;
      transform: translateY(-50%);
      background: linear-gradient(0.25turn, #ec5b54, #ffcd00, #86bc25);
      border-radius: 5px;
    }

    .v-slider__track-background {
      border-radius: 5px;
      background: transparent !important;
    }

    .v-slider__track-fill {
      border-radius: 5px;
      background: transparent !important;
    }
  }
}
</style>
