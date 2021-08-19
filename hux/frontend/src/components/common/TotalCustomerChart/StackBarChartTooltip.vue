<template>
  <div>
    <v-card
      v-if="showTooltip"
      tile
      :style="{
        transform: `translate(${position.x}px, ${position.y}px)`,
        'border-radius': '0px !important',
      }"
      class="mx-auto description-tooltip-style"
    >
      <div class="bar-hover neroBlack--text">
        <span class="feature-name">
          {{ sourceInput.name }}
        </span>
        <span class="feature-description">
          {{ sourceInput.description }}
        </span>
      </div>
    </v-card>
  </div>
</template>

<script>
export default {
  name: "stack-bar-chart-tooltip",
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
  padding: 7px 20px 20px 20px;
}

.description-tooltip-style {
  @extend .box-shadow-3;
  border-radius: 0px;
  max-width: 230px;
  height: auto;
  top: -620px;
  left: -230px;
  z-index: 1;
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
</style>
