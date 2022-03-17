<template>
  <v-card class="card-style" shaped outlined>
    <v-card-text class="text-style">
      {{ value }}
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
  width: 40px;
  height: 40px;
  border-color: blue;
  border-radius: 0 !important;
  border-width: thick;
}
.text-style {
  // num style
  font: Open Sans SemiBold;
  font-weight: 600;
  font-style: normal;
  font-size: 16px;
  word-wrap: normal;
  transform: translate(0%, 35%) rotate(-45deg);
  padding: 0px;
  display: block;
  text-align: center;
}
</style>
