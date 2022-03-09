<template>
  <div class="num-style">{{ value }}</div>
</template>

<script>
export default {
  name: "RhombusNumber",
  props: {
    value: {
      type: Number,
      required: true,
    },
  },
}
</script>

<style lang="scss" scoped>
.num-style {
  font: Open Sans SemiBold;
  font-weight: 600;
  font-style: normal;
  font-size: 16px;
  line-height: 21.79px;
  text-align: center;
}
</style>
