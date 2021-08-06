<template>
  <div class="container">
    <div class="d-flex justify-content-start">
      <line-area-chart
      v-model="spendData"
      />
    </div>
  </div>
</template>

<script>
import LineAreaChart from "@/components/common/areaChart/LineAreaChart"
//TODO: API Integration
import data from "./areaChart.json"

export default {
  name: "area-chart",
  components: { LineAreaChart },
  data() {
    return {
      show: false,
      tooltip: {
        x: 0,
        y: 0,
      },
      spendData: data.spend,
    }
  },
}
</script>

<style lang="scss" scoped>
.global-text-line {
  display: inline-block;
  font-style: normal;
  font-size: $font-size-root;
  line-height: 19px;
}
.container {
  height: 350px;
  padding: 0px !important;
}
</style>
