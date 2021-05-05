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
              v-for="(item, index) in 2"
              :key="index"
            >
              <Logo :type="cellValue.details[index].type" :size="18"></Logo>
            </v-btn>
            <div class="extra-icon mr-1" v-show="cellValue.details.length > 2">
              +{{ cellValue.details.length - 2 }}
            </div>
          </v-col>
        </v-row>
      </div>
    </template>
    <v-list v-show="cellValue.details.length > 2">
      <v-list-item
        v-for="(item, index) in cellValue.details"
        :key="index"
        v-show="index > 1"
      >
        <v-list-item-title>
          <v-btn class="mr-1" width="18" height="18" outlined fab>
            <Logo :type="item.type" :size="18"></Logo>
          </v-btn>
          {{ item.name }}
        </v-list-item-title>
      </v-list-item>
    </v-list>
  </v-menu>
</template>
<script>
import Vue from "vue"
import Logo from "@/components/common/Logo"

export default Vue.extend({
  name: "DestinationCell",
  components: {
    Logo,
  },
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
