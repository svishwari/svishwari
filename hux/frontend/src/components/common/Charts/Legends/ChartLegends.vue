<template>
  <div
    class="chart-legends"
  >
    <span class="legends" :style="{ backgroundColor: item.color }" v-for="item in legendsData" :key="item.text" >{{item.text}}</span>
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
  .legends {
    margin-right: 20px;
  height: 25px;
  width: 25px;
  background-color: #bbb;
  border-radius: 50%;
  display: inline-block;

  }
}

.chart-tooltip {
  padding: 6px 16px;
  position: fixed;
  background: var(--v-white-base);
  @extend .box-shadow-25;
}
</style>
