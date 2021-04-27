<template>
  <v-row class="destination-cell-wrapper">
    <v-col class="d-flex align-center pr-0 mt-2">
      <v-btn class="mr-1" width="18" height="18" outlined fab>
        <img src="../../../assets/images/facebook.png" alt="mailchimp" />
      </v-btn>
      <v-btn class="mr-1" width="18" height="18" outlined fab>
        <img src="../../../assets/images/mailchimp.png" alt="mailchimp" />
      </v-btn>
      <div class="extra-icon mr-1">+2</div>
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
      evnt.preventDefault()
    },
    takeActions(evnt) {
      evnt.preventDefault()
    },
  },
})
</script>
<style lang="scss" scoped>
.destination-cell-wrapper {
}
</style>
