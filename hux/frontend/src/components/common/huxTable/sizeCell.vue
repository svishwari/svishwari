<template>
  <v-menu bottom offset-y open-on-hover>
    <template v-slot:activator="{ on, attrs }">
      <span v-bind="attrs" v-on="on" class="cursor-default">
        {{ cellValue.approxSize }}
      </span>
    </template>
    <v-list>
      <v-list-item>
        <v-list-item-title>{{ cellValue.actualSize }}</v-list-item-title>
      </v-list-item>
    </v-list>
  </v-menu>
</template>
<script>
import Vue from "vue"
export default Vue.extend({
  name: "sizeCell",
  data() {
    return {
      cellValue: null,
    }
  },
  beforeMount() {
    if (this.params.value) {
      this.cellValue = {
        approxSize: this.getApproxSize(this.params.value),
        actualSize: this.params.value,
      }
    } else {
      this.cellValue = {
        approxSize: "",
        actualSize: "",
      }
    }
  },
  methods: {
    getApproxSize(value) {
      // Nine Zeroes for Billions
      return Math.abs(Number(value)) >= 1.0e9
        ? (Math.abs(Number(value)) / 1.0e9).toFixed(2) + "B"
        : // Six Zeroes for Millions
        Math.abs(Number(value)) >= 1.0e6
        ? (Math.abs(Number(value)) / 1.0e6).toFixed(2) + "M"
        : // Three Zeroes for Thousands
        Math.abs(Number(value)) >= 1.0e3
        ? (Math.abs(Number(value)) / 1.0e3).toFixed(2) + "K"
        : Math.abs(Number(value))
    },
  },
})
</script>
<style lang="scss" scoped></style>
