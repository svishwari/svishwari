<template>
  <v-card max-width="200" height="104" :style="{ 'top': positionTop+'px', 'left':positionLeft+'px' }" tile class="rounded-lg card-style">
      Test Data

      top: {{positionTop}}

      left: {{positionLeft}}
  </v-card>
</template>

<script>
export default {
  name: "ChartTooltip",
  props: {
    positionTop: {
      type: Number,
      required: false,
    },
    positionLeft: {
      type: Number,
      required: false,
    },
  },
}
</script>

<style lang="scss" scoped>
.card-style {
    max-width: 308px;
    max-height: 20px;
}
</style>
