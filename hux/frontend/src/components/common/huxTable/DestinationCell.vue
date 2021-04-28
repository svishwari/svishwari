<template>
  <v-menu bottom offset-y open-on-hover>
    <template v-slot:activator="{ on, attrs }">
      <div v-bind="attrs" v-on="on">
        <v-row class="destination-cell-wrapper">
          <v-col class="d-flex align-center pr-0 mt-2">
            <v-btn
              class="mr-1"
              width="18"
              height="18"
              outlined
              fab
              v-for="(item, index) in cellValue.details"
              :key="index"
            >
              <img src="../../../assets/images/facebook.png" alt="mailchimp" />
            </v-btn>
            <div class="extra-icon mr-1">+2</div>
          </v-col>
        </v-row>
      </div>
    </template>
    <v-list>
      <v-list-item v-for="(item, index) in cellValue.details" :key="index">
        <v-list-item-title>
          <v-btn class="mr-1" width="18" height="18" outlined fab>
            <img src="../../../assets/images/facebook.png" alt="mailchimp" />
          </v-btn>
          Facebook
        </v-list-item-title>
      </v-list-item>
    </v-list>
  </v-menu>
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
