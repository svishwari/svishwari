<template>
  <div
    class="chart-legends"
  >
  <span class="legends" v-for="item in legendsData" :key="item.text">
    <span class="dots" :style="{ backgroundColor: item.color }"></span><span class="text">{{item.text}}</span>
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
      default: [
        {color: "rgba(0, 85, 135, 1)", text: "Women"},
        {color: "rgba(12, 157, 219, 1)", text: "Men"},
        {color: "rgba(66, 239, 253, 1)", text: "Other"}
      ]
    },
  },
}
</script>
<style lang="scss" scoped>
.chart-legends {
  .legends {
    margin-right: 10px;
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
    }
  }
}
</style>
