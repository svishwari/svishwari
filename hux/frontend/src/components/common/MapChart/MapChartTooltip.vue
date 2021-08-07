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
        {{ sourceInput.name }}
      </span>
      <div class="sub-props pt-4">
        <span class="subprop-name">Size</span>
        <span class="value ml-1">{{ sourceInput.size | Empty }}</span>
      </div>
      <div class="sub-props pt-4">
        <span class="subprop-name">W/M/O</span>
        <span class="value ml-1">
          {{ sourceInput.women | Numeric(true, false, false, true) | Empty }} |
          {{ sourceInput.men | Numeric(true, false, false, true) | Empty }} |
          {{ sourceInput.other | Numeric(true, false, false, true) | Empty }}
        </span>
      </div>
      <div class="sub-props pt-4">
        <span class="subprop-name">LTV</span>
        <span class="value ml-1">{{ sourceInput.ltv | Currency | Empty }}</span>
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
  padding: 10px 20px 20px 20px;
}

.tooltip-style {
  @extend .box-shadow-3;
  border-radius: 0px;
  max-width: 213px;
  height: auto;
  top: -500px;
  left: -660px;
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
