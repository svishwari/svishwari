<template>
  <v-card class="card-style" shaped outlined>
    <v-card-text class="text-style">
      <div>{{ value }}</div>
    </v-card-text>
  </v-card>
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
  transform: rotate(45deg);
  max-width: 54px;
  max-height: 54px;
}
.text-style {
  // num style
  font: Open Sans SemiBold;
  font-weight: 600;
  font-style: normal;
  font-size: 16px;
  line-height: 21.79px;
  text-align: center;
  transform: rotate(-45deg);
}
</style>
