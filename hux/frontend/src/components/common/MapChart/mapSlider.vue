<template>
  <v-slider class="hux-score-slider" always-dirty readonly @end="onFinalValue">
    <template #append>
      <span class="slider-value-display" v-text="minValue"></span>
    </template>
    <template #prepend>
      <span class="slider-value-display" v-text="maxValue"></span>
    </template>
  </v-slider>
</template>

<script>
export default {
  name: "map-slider",
  props: {
    min: {
      type: Number,
      default: 0.2345,
      required: false,
    },
    max: {
      type: Number,
      default: 0.90023,
      required: false,
    },
  },
   data() {
    return {
      minValue: this.$options.filters
              .percentageConvert(this.min, true, true),
      maxValue: this.$options.filters
              .percentageConvert(this.max, true, true)
    }
  },
}
</script>

<style lang="scss" scoped>
.hux-range-slider {
  ::v-deep .v-input__control {
    .v-input__slot {
      .v-slider__track-container {
        height: 7px;
      }
      .lighten-3 {
        background-color: rgba(157, 212, 207, 0.25) !important;
      }
      .theme--light {
        .v-slider__track-fill {
          background-color: var(--v-persianGreen-base) !important;
        }
      }
      .v-slider__thumb {
        display: none;
      }
      .v-slider__thumb-label {
        display: none;
      }
    }
  }
}
.hux-score-slider {
  margin-right: 10px;
  transform: rotate(90deg);
  max-width: 140px;
  margin-left: 600px;
  margin-top: -140px;

  .slider-value-display {
    width: 28px;
    height: 16px;
    color: black;
    transform: rotate(-90deg);
  }

  ::v-deep .v-application--is-ltr v-input__prepend-outer {
    margin-right: 2px;
  }

  ::v-deep .v-slider__thumb {
    display: none;

    &:before {
      left: -10px;
      top: -10px;
    }
  }

  ::v-deep .v-slider--horizontal {
    margin-left: 0px;

    .v-slider__track-container {
      width: 101%;
      height: 11px;
      left: -6px;
      transform: translateY(-50%);
      background: linear-gradient(0.25turn, #396286, #ffffff);
      border: 1px solid rgba(0, 124, 176, 0.2);
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
