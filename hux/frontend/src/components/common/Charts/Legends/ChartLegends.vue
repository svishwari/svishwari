<template>
  <div>
    <span v-for="item in legendsData" :key="item.text" class="chart-legends">
      <span class="legend-items"
        ><span class="dots" :style="{ backgroundColor: item.color }"></span
        ><span class="text">{{ item.text }}</span></span
      >
    </span>
  </div>
</template>

<script>
export default {
  name: "ChartLegends",
  props: {
      /**
     * Accepts an array of object consist of Label circle color & text
     * eg:  [{ color: "rgba(208, 208, 206, 1)", text: "no data available" }]
     */
    legendsData: {
      type: Array,
      required: true,
    },
  },
}
</script>
<style lang="scss" scoped>
.chart-legends {
  margin-right: 10px;
  display: inline-block;
  .legend-items {
    display: flex;
    justify-content: flex-start;
    align-items: center;
    .dots {
      margin-right: 5px;
      height: 12px;
      width: 12px;
      border-radius: 50%;
      display: inline-block;
    }
    .text {
      font-size: 12px;
      color: var(--v-black-darken1);
      display: inline-block;
    }
  }
}
</style>
