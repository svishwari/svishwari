<template>
  <div
    v-if="showTooltip"
    class="tooltip"
    :style="{
      transform: `translate(${tooltip.x}px, ${tooltip.y}px)`,
    }"
  >
    <v-card tile>
      <div class="type mb-1">
        <span v-if="sourceInput.label == 'Men'" class="circle-men"></span>
        <span v-if="sourceInput.label == 'Women'" class="circle-women"></span>
        <span v-if="sourceInput.label == 'Other'" class="circle-other"></span>

        <span
          v-if="sourceInput.label == 'Men'"
          class="primary--text text--darken-1"
        >
          {{ sourceInput.label }}
        </span>
        <span v-if="sourceInput.label == 'Women'" class="primary--text">
          {{ sourceInput.label }}
        </span>
        <span
          v-if="sourceInput.label == 'Other'"
          class="primary--text text--lighten-7"
        >
          {{ sourceInput.label }}
        </span>
      </div>
      <div class="percentage black--text text--darken-4">
        {{ getPercentage(sourceInput.population_percentage) }}
      </div>
      <div class="value black--text text--darken-4">{{ sourceInput.size }}</div>
    </v-card>
  </div>
</template>

<script>
export default {
  name: "DoughnutChartTooltip",
  props: {
    tooltip: {
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
  methods: {
    getPercentage(data) {
      return parseInt((data * 100).toFixed(0)) + "%"
    },
  },
}
</script>

<style lang="scss" scoped>
.circle {
  height: 9px;
  border-radius: 9px;
  width: 9px;
  float: left;
  margin-top: 7px;
  margin-right: 3px;
}
.tooltip {
  width: 82px !important;
  height: 64px;
  position: absolute;
  .v-card {
    padding: 8px 8px;
    @extend .box-shadow-25;
    .circle-men {
      @extend .circle;
      border: 2px solid var(--v-primary-darken1);
    }
    .circle-other {
      @extend .circle;
      border: 2px solid var(--v-primary-lighten7);
    }
    .circle-women {
      @extend .circle;
      border: 2px solid var(--v-primary-base);
    }
  }
}
</style>
