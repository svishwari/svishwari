<template>
  <div>
    <v-card
      v-if="showTooltip"
      tile
      :style="{
        transform: `translate(${sourceInput.xPosition}px, ${sourceInput.yPosition}px)`,
        'border-radius': '0px !important',
      }"
      class="mx-auto tooltip-style"
    >
      <div class="bar-hover">
        {{ sourceInput.ltv | Currency }}
      </div>
    </v-card>
  </div>
</template>

<script>
export default {
  name: "BarChartTooltip",
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

.global-text-line {
  display: inline-block;
  font-weight: normal;
  font-style: normal;
  font-size: 12px;
  line-height: 16px;
  color: var(--v-black-darken2) !important;
}

.card-padding {
  padding: 10px 0px 0px 13px;
}

.income-tooltip-style {
  @extend .box-shadow-3;
  border-radius: 0px;
  height: auto;
  z-index: 1;
  color: #0c9ddb;
  .bar-hover {
    @extend .card-padding;
  }
}

.tooltip-style {
  @extend .income-tooltip-style;
  max-width: 70px;
  height: 40px;
  top: -400px;
  left: -90px;
  z-index: 1;
}
</style>
