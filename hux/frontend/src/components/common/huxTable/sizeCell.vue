<template>
  <v-menu bottom offset-y open-on-hover>
    <template v-slot:activator="{ on, attrs }">
      <div v-bind="attrs" v-on="on">
        {{ cellValue.approxSize }}
      </div>
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
    this.cellValue = this.getValueToDisplay(this.params)
  },
  methods: {
    getValueToDisplay(params) {
      return params.valueFormatted ? params.valueFormatted : params.value
    },
  },
})
</script>
<style lang="scss" scoped></style>
