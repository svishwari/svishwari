<template>
  <v-card
    v-if="showTooltip"
    tile
    :style="{
      transform: `translate(${position.x}px, ${position.y}px)`,
      'border-radius': '0px !important',
    }"
    class="mx-auto tooltip-style"
  >
    <div class="map-hover">
      <span class="prop-name font-weight-semi-bold">
        {{ sourceInput[defaultMetric] }}
      </span>
      <div
        class="sub-props pt-4"
        v-for="metric in configurationData.tooltip_metrics"
        :key="metric.label"
      >
        <span v-if="metric.is_Combined_Metric" class="subprop-name">{{
          metric.label
        }}</span>
        <span v-if="!metric.is_Combined_Metric" class="subprop-name">{{
          metric.label
        }}</span>
        <span v-if="metric.is_Combined_Metric" class="value ml-1">
          <span v-for="(value, index) in metric.key" :key="value">
            {{ applyFilter(sourceInput[value], metric.format) }}
            <span v-if="index !== metric.key.length - 1">|</span>
          </span>
        </span>
        <span v-if="!metric.is_Combined_Metric" class="value ml-1">
          {{ applyFilter(sourceInput[metric.key], metric.format) }}
        </span>
      </div>
    </div>
  </v-card>
</template>

<script>
export default {
  name: "MapChartTooltip",
  props: {
    position: {
      type: Object,
      required: false,
      default() {
        return {
          x: 0,
          y: 0,
        }
      },
    },
    showTooltip: {
      type: Boolean,
      required: false,
      default: false,
    },
    sourceInput: {
      type: Object,
      required: false,
    },
    configurationData: {
      type: Object,
      required: true,
    },
  },
  computed: {
    defaultMetric() {
      return this.configurationData.default_metric.key
    },
  },
  methods: {
    applyFilter(value, filter) {
      switch (filter) {
        case "numeric":
          return this.$options.filters.Numeric(value, true, false, false)
        case "percentage":
          return this.$options.filters.Numeric(value, true, false, false, true)
        case "currency":
          return this.$options.filters.Currency(value)
        default:
          return this.$options.filters.Empty
      }
    },
  },
}
</script>

<style lang="scss" scoped>
::v-deep .v-card {
  border-radius: 0px !important;
}
.global-heading {
  @extend .font-weight-semi-bold;
  font-style: normal;
  font-size: $font-size-root;
  line-height: 19px;
  padding-left: 2px;
}

.global-text-line {
  display: inline-block;
  font-weight: normal;
  font-style: normal;
  font-size: 12px;
  line-height: 16px;
}

.card-padding {
  padding: 10px !important;
}

.tooltip-style {
  @extend .box-shadow-3;
  border-radius: 0px;
  max-width: 213px;
  min-width: 210px;
  height: auto;
  position: absolute;
  top: -160px;
  left: -240px;
  z-index: 1;
  .map-hover {
    @extend .card-padding;
    .prop-name {
      @extend .global-heading;
    }
    .sub-props {
      display: flex;
      justify-content: flex-end;
      align-items: center;
      height: 30px;
      .subprop-name {
        @extend .global-text-line;
        flex: 0 0 40%;
        padding-left: 5px;
      }
      .value {
        @extend .global-text-line;
        flex: 1;
        text-align: left;
      }
    }
  }
}
</style>
