<template>
  <v-menu bottom offset-y open-on-hover class="cursor-default">
    <template v-slot:activator="{ on, attrs }">
      <v-btn color="blue-grey" small outlined fab v-bind="attrs" v-on="on">
        {{ cellValue.shortName }}
      </v-btn>
    </template>
    <v-list>
      <v-list-item>
        <v-list-item-title>{{ cellValue.fullName }}</v-list-item-title>
      </v-list-item>
    </v-list>
  </v-menu>
</template>
<script>
import Vue from "vue"
export default Vue.extend({
  name: "UserAvatarCell",
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
.blue-grey--text {
  border-width: 2px;
  font-size: 14px;
  line-height: 22px;
  border-color: var(--v-info-base);
  color: var(--v-neroBlack-base) !important;
  cursor: default !important;
}
</style>
