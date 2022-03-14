<template>
  <v-card-text class="card-style">
    <div>{{ value }}</div>
  </v-card-text>
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
.card-style {
  // num style
  font: Open Sans SemiBold;
  font-weight: 600;
  font-style: normal;
  font-size: 16px;
  line-height: 21.79px;
  text-align: center;
  // card style
  width: 50px;
  height: 50px;
}
</style>
