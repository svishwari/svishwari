<template>
  <v-row class="destination-cell-wrapper">
    <v-col class="d-flex pr-0">
      {{ cellValue }}
      <!-- <img src="../../../assets/images/mailchimp.png" alt="Girl in a jacket" width="18" height="18"> -->
    </v-col>
  </v-row>
</template>
<script>
import Vue from "vue"
export default Vue.extend({
  name: "DestinationCell",
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
    addToFavorite(evnt) {
      evnt.preventDefault();
    },
    takeActions(evnt) {
      evnt.preventDefault();
    }
  },
})
</script>
<style lang="scss" scoped>
.destination-cell-wrapper {

}
</style>
