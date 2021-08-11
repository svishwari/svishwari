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
        <div>
          <span class="append-circle color-women"></span
          ><span class="font-size-tooltip">{{ sourceInput.women_spend | currency }}</span>
        </div>
        <div>
          <span class="append-circle color-men"></span
          ><span class="font-size-tooltip">{{ sourceInput.men_spend | currency }}</span>
        </div>
        <div>
          <span class="append-circle color-other"></span
          ><span class="font-size-tooltip">{{ sourceInput.others_spend | currency }}</span>
        </div>
      </div>
    </v-card>
  </div>
</template>

<script>
export default {
  name: "AreaChartTooltip",
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
  top: -420px;
  left: -242px;
  z-index: 1;
}
.append-circle {
  height: 15px;
  width: 15px;
  background-color: #fff;
  border-radius: 50%;
  display: inline-block;
  margin-top: 10px;
  margin-right: 8px;
}
.color-women {
  border: 1px solid rgba(0, 85, 135, 1);
}
.color-men {
  border: 1px solid #0c9ddb;
}
.color-other {
  border: 1px solid #42effd;
}
.font-size-tooltip {
  font-family: Open Sans;
font-style: normal;
font-weight: normal;
font-size: 12px;
line-height: 16px;
color: #4F4F4F;
}
</style>
