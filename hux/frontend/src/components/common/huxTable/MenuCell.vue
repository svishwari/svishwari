<template>
  <v-row class="menu-cell-wrapper d-flex align-start">
    <span class="font-weight-light ml-2 mt-1">
      {{ cellValue }}
    </span>
    <v-spacer></v-spacer>
    <span class="font-weight-light ml-2 mt-1 float-right"> View </span>
  </v-row>
</template>
<script>
import Vue from "vue"
export default Vue.extend({
  name: "MenuCell",
  data() {
    return {
      cellValue: null,
    }
  },
  beforeMount() {
    this.cellValue = this.getValueToDisplay(this.params)
  },
  methods: {
    getValueToDisplay(params) {
      return params.valueFormatted ? params.valueFormatted : params.value
    },
  },
})
</script>
<style lang="scss" scoped>
</style>
