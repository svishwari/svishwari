<template>
  <v-slider
    v-if="mapData.length != 0"
    class="hux-map-slider"
    always-dirty
    readonly
  >
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
    mapData: {
      type: Array,
      required: false,
    },
    configurationData: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      minValue: "-%",
      maxValue: "-%",
    }
  },
  computed: {
    primaryMetric() {
      return this.configurationData.primary_metric.key
    },
  },
  async mounted() {
    await this.mapData
    let total_range = this.mapData.map((data) => data[this.primaryMetric])
    let maximumRange = Math.max(...total_range)
    this.minValue = this.$options.filters.Percentage(0)
    this.maxValue = maximumRange
      ? this.$options.filters.Percentage(maximumRange)
      : "100%"
  },
}
</script>

<style lang="scss" scoped>
.hux-map-slider {
  margin-right: 10px;
  transform: rotate(90deg);
  max-width: 138px;
  margin-right: -27px;
  margin-top: 68px;
  float: right;
  ::v-deep {
    .v-input__control {
      .v-input__slot {
        min-width: 75px;
      }
    }
    .v-input__prepend-outer,
    .v-input__append-outer {
      margin-top: 0px;
    }
  }
  .slider-value-display {
    width: 31px;
    height: 16px;
    color: var(--v-black-darken4);
    transform: rotate(-90deg);
    font-size: 12px;
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
        var(--v-primary-darken4),
        var(--v-white-base)
      );
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
