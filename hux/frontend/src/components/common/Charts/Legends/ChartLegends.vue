<template>
  <div
    class="chart-legends"
  >
  <span class="legends" v-for="item in legendsData" :key="item.text">
    <span class="dots" :style="{ backgroundColor: item.color }"></span><span>{{item.text}}</span>
  </span>
  </div>
</template>

<script>
export default {
  name: "ChartLegends",
  props: {
    legendsData: {
      type: Array,
      required: false,
    },
  },
}
</script>
<style lang="scss" scoped>
.chart-legends {
  margin-top: 20px;
  .legends {
    margin-right: 10px;
    .dots {
    margin-top: 20px;
    margin-right: 5px;
  height: 10px;
  width: 10px;
  background-color: #bbb;
  border-radius: 50%;
  display: inline-block;
    }
  }
}

.chart-tooltip {
  padding: 6px 16px;
  position: fixed;
  background: var(--v-white-base);
  @extend .box-shadow-25;
}
</style>
