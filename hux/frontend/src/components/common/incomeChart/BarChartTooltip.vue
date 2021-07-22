<template>
  <div>
    <v-card
      v-if="showTooltip"
      tile
      :style="{
        transform: `translate(${position.x}px, ${position.y}px)`,
        'border-radius': '0px !important',
      }"
      class="mx-auto score-tooltip-style"
    >
      <div class="bar-hover">
        {{ sourceInput.ltv | Currency}}
      </div>
    </v-card>
  </div>
</template>

<script>
export default {
  name: "bar-chart-tooltip",
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
  color: var(--v-darkGreyHeading-base) !important;
}

.card-padding {
  padding: 10px 20px 20px 10px;
}

.description-tooltip-style {
  @extend .box-shadow-3;
  border-radius: 0px;
  max-width: 230px;
  height: auto;
  z-index: 1;
  color: #0C9DDB;
  .bar-hover {
    @extend .card-padding;
    .feature-name {
      @extend .global-text-line;
    }
    .feature-description {
      @extend .global-text-line;
      margin-top: 8px;
    }
  }
}

.score-tooltip-style {
  @extend .description-tooltip-style;
  max-width: 100px;
  height: 40px;
  top: -350px;
  left: -60px;
  z-index: 1;
}
</style>
