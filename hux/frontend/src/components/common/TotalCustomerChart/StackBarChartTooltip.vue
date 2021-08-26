<template>
  <v-card
    v-if="showToolTip"
    tile
    :style="{
      transform: `translate(${sourceInput.xPosition}px, ${sourceInput.yPosition}px)`,
      left: sourceInput.isEndingBar ? '-136px' : '49px'
    }"
    class="mx-auto tooltip-style"
  >
    <div class="neroBlack--text caption">
      <div class="value-section">
        {{ sourceInput.date | Date("MM/DD/YYYY") }}
      </div>
      <div class="value-container">
        <icon
          type="name"
          :size="12"
          :fill-opacity="0.5"
          :color="colorCodes[sourceInput.index]"
        />
        <span class="text-label">Total customers</span>
      </div>
      <div class="value-section">
        {{ sourceInput.totalCustomers | Numeric(true, false, false) }}
      </div>
      <div class="value-container">
        <icon type="name" :size="12" :color="colorCodes[sourceInput.index]" />
        <span class="text-label">New customers added</span>
        <div class="value-section">
          {{ sourceInput.addedCustomers | Numeric(true, false, false) }}
        </div>
      </div>
    </div>
  </v-card>
</template>

<script>
import Icon from "@/components/common/Icon"

export default {
  name: "StackBarChartTooltip",
  components: { Icon },
  props: {
    showToolTip: {
      type: Boolean,
      required: false,
      default: false,
    },
    sourceInput: {
      type: Object,
      required: false,
    },
    colorCodes: {
      type: Array,
      required: true,
    },
  },
}
</script>

<style lang="scss" scoped>
::v-deep .v-card {
  border-radius: 0px !important;
}

.global-heading {
  font-style: normal;
  font-size: 12px;
  line-height: 19px;
}

.tooltip-style {
  @extend .box-shadow-3;
  border-radius: 0px;
  padding: 8px 8px 15px 8px;
  max-width: 172px;
  height: 112px;
  z-index: 1;
  border-radius: 0px !important;
  position: absolute;
  top: -38px;
  .value-container {
    margin-top: 2px;
    @extend .global-heading;
    .text-label {
      margin-left: 8px !important;
    }
  }

  .value-section {
    @extend .global-heading;
    margin-left: 21px;
  }
}
</style>
