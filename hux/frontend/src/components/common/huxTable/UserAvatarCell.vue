<template>
  <v-btn color="blue-grey" small outlined fab>
    {{ cellValue }}
  </v-btn>
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
<style lang="scss" scoped></style>
