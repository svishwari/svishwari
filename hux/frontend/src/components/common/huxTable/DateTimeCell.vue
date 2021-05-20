<template>
  <v-menu bottom offset-y open-on-hover class="cursor-default">
    <template v-slot:activator="{ on, attrs }">
      <span v-bind="attrs" v-on="on" class="cursor-default">
        {{ cellValue.shortDate }}
      </span>
    </template>
    <v-list>
      <v-list-item>
        <v-list-item-title>{{
          cellValue.FullDate ? cellValue.FullDate : ""
        }}</v-list-item-title>
      </v-list-item>
    </v-list>
  </v-menu>
</template>
<script>
import Vue from "vue"
export default Vue.extend({
  name: "DateTimeCell",
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
