<template>
  <div>
    <v-card
     v-if="showTooltip"
      tile
      :style="{
        transform: `translate(${position.x}px, ${position.y}px)`,
        'border-radius': '0px !important',
      }"
      class="mx-auto tooltip-style"
    >
      <div class="bar-hover">
        <!-- {{sourceInput.date | Date("relative")}} -->
        {{sourceInput.women_spend | currency}}
        {{sourceInput.men_spend | currency}}
        {{sourceInput.others_spend | currency}}
      </div>
    </v-card>
  </div>
</template>

<script>
export default {
  name: "area-chart-tooltip",
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
      required: true,
      default: true,
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
  color: var(--v-darkGreyHeading-base) !important;
}

.card-padding {
  padding: 10px 0px 0px 13px;
}

.income-tooltip-style {
  @extend .box-shadow-3;
  border-radius: 0px;
  height: auto;
  z-index: 1;
  color: var(--v-grey-base);
  .bar-hover {
    @extend .card-padding;
  }
}

.tooltip-style {
  @extend .income-tooltip-style;
  max-width: 96px;
  height: 104px;
         top: -366px;
    left: -258px;
  z-index: 1;
}
</style>
