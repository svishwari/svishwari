<template>
  <div class="chart-wrapper text-center mt-14">
    <div class="chart-image">
      <slot name="chart-image"></slot>
    </div>
    <div class="ruler-image">
      <img src="@/assets/images/pencil-ruler.png" alt="pencil-ruler" />
    </div>
    <div class="chart-title">Exciting visuals are in the works!</div>
    <div class="text-subtitle-1">
      Hang tight as our devs work hard to update this section
    </div>
  </div>
</template>

<script>
export default {
  name: "EmptyStateChart",
}
</script>
<style lang="scss" scoped>
.chart-wrapper {
  .chart-image {
    min-width: 400px;
  }
  .chart-title {
    font-weight: 300;
    font-size: 18px;
    line-height: 24px;
  }
}
</style>
