<template>
  <v-menu bottom offset-y open-on-hover>
    <template #activator="{ on, attrs }">
      <span v-bind="attrs" v-on="on">
        {{ cellValue.attribute }}
      </span>
    </template>
    <v-list>
      <v-list-item
        v-for="(item, index) in cellValue.attributeList"
        :key="index"
      >
        <v-list-item-title>{{ item.attribute }}</v-list-item-title>
      </v-list-item>
    </v-list>
  </v-menu>
</template>
<script>
import Vue from "vue"
export default Vue.extend({
  name: "AttributeCell",
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
