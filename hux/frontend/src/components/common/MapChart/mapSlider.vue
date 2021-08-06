<template>
  <v-slider class="hux-map-slider" always-dirty readonly>
    <template #append>
      <span
        class="slider-value-display font-weight-semi-bold"
        v-text="minValue"
      ></span>
    </template>
    <template #prepend>
      <span
        class="slider-value-display font-weight-semi-bold"
        v-text="maxValue"
      ></span>
    </template>
  </v-slider>
</template>

<script>
export default {
  name: "MapSlider",
  props: {
    min: {
      type: Number,
      required: false,
    },
    max: {
      type: Number,
      required: false,
    },
  },
  data() {
    return {
      minValue: this.min ? this.$options.filters.Percentage(this.min) : "-%",
      maxValue: this.max ? this.$options.filters.Percentage(this.max) : "-%",
    }
  },
}
</script>

<style lang="scss" scoped>
.hux-map-slider {
  margin-right: 10px;
  transform: rotate(90deg);
  max-width: 140px;
  margin-left: 655px;
  margin-top: -115px;
  ::v-deep .v-input__control {
    .v-input__slot {
      min-width: 75px;
    }
  }
  .slider-value-display {
    width: 30px;
    height: 16px;
    color: var(--v-neroBlack-base);
    transform: rotate(-90deg);
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
      background: linear-gradient(
        0.25turn,
        var(--v-tealBlue-base),
        var(--v-white-base)
      );
      border: 1px solid var(--v-anchor-base);
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
