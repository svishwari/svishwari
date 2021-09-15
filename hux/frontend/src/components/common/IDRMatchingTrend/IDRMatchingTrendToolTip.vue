<template>
  <v-card
    v-if="showToolTip"
    tile
    :style="{
      transform: `translate(${sourceInput.xPosition}px, ${sourceInput.yPosition}px)`,
    }"
    class="mx-auto tooltip-style"
  >
    <div class="neroBlack--text caption">
      <div class="value-section">
        <div class="date-font">
          {{ sourceInput.date | Date("MMM DD[,] YYYY") }}
        </div>
        <div>
          <span class="append-circle color-known-ids"></span>
          <span class="font-size-tooltip">
            {{ sourceInput.known_ids | Numeric(false, false, true) | Empty }}
          </span>
        </div>
        <div>
          <span class="append-circle color-unique-hux-ids"></span>
          <span class="font-size-tooltip">
            {{
              sourceInput.unique_hux_ids | Numeric(false, false, true) | Empty
            }}
          </span>
        </div>
        <div>
          <span class="append-circle color-anonymous-ids"></span>
          <span class="font-size-tooltip">
            {{
              sourceInput.anonymous_ids | Numeric(false, false, true) | Empty
            }}
          </span>
        </div>
      </div>
    </div>
  </v-card>
</template>

<script>
export default {
  name: "IDRMatchingTrendTooltip",
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
  height: auto;
  z-index: 1;
  border-radius: 0px !important;
  position: absolute;
  top: -100px;
  left: 69px;
  .value-container {
    margin-top: 2px;
    @extend .global-heading;
    .text-label {
      margin-left: 8px !important;
    }
  }
  .value-section {
    @extend .global-heading;
  }
  .item_count {
    font-weight: bold;
  }
  .append-circle {
    height: 12px;
    width: 12px;
    background-color: #fff;
    border-radius: 50%;
    display: inline-block;
    margin-top: 6px;
    margin-right: 8px;
  }
  .color-known-ids {
    border: 2px solid #42effd;
  }
  .color-anonymous-ids {
    border: 2px solid #75787b;
  }
  .color-unique-hux-ids {
    border: 2px solid #347dac;
  }
}
</style>
