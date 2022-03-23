<template>
  <v-card class="card-style" :style="style" shaped outlined>
    <v-card-text class="text-subtitle-1 text-style">
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
    color: {
      type: String,
      required: false,
      default: "green",
    },
  },
  computed: {
    style() {
      return "border-color: " + this.color
    },
  },
}
</script>

<style lang="scss" scoped>
.card-style {
  transform: rotate(45deg);
  width: 30px;
  height: 30px;
  border-radius: 0 !important;
  border-width: 2px;
}
.text-style {
  // num style
  color: black !important;
  line-height: 16px;
  transform: translate(0%, 25%) rotate(-45deg);
  padding: 0px;
  display: block;
  text-align: center;
}
</style>
