<template>
  <div
    class="tooltip"
    :style="{
      transform: `translate(${tooltip.x}px, ${tooltip.y}px)`,
      'border-radius': '0px !important',
    }"
    v-if="showTooltip"
  >
    <v-card>
      <div class="type mb-1">
        <span class="circle-men" v-if="sourceInput.label == 'Men' "></span>
        <span class="circle-women" v-if="sourceInput.label == 'Women' "></span>
        <span class="circle-other" v-if="sourceInput.label == 'Other' "></span>

        <span v-if="sourceInput.label == 'Men' " class="royalBlue--text"> {{sourceInput.label}} </span>
        <span v-if="sourceInput.label == 'Women' " class="primary--text"> {{sourceInput.label}} </span>
        <span v-if="sourceInput.label == 'Other' " class="oceanBlue--text"> {{sourceInput.label}} </span>
      </div>
      <div class="percentage neroBlack--text">{{ getPercentage(sourceInput.population_percentage) }}</div>
      <div class="value neroBlack--text">{{sourceInput.size}}</div>
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
    getPercentage(data){
      return parseInt((data * 100).toFixed(0)) + '%'
    }
  },
}
</script>

<style lang="scss" scoped>
.circle {
  height: 12px;
  border-radius: 12px;
  width: 12px;
  float: left;
  margin-top: 3px;
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
        border: 1px solid var(--v-royalBlue-base);
      }
      .circle-other {
        @extend .circle;
        border: 1px solid var(--v-oceanBlue-base);
      }
      .circle-women {
        @extend .circle;
        border: 1px solid var(--v-primary-base);
      }
    }
  }
</style>
