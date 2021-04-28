<template>
  <div class="status-wrapper">
    <v-icon v-if="cellValue == 'Active'" class="material-icons delivered">
      mdi-checkbox-blank-circle
    </v-icon>
    <v-icon v-if="cellValue == 'Delivering'" class="material-icons delivering">
      mdi-circle-double
    </v-icon>
    <v-icon v-if="cellValue == 'Error'" class="material-icons alert">
      mdi-alert-circle
    </v-icon>
    <span class="value">
      {{ cellValue }}
    </span>
  </div>
</template>
<script>
import Vue from "vue"
export default Vue.extend({
  name: "StatusCell",
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
.status-wrapper {
  .material-icons.delivered {
    color: #43b02a;
  }
  .material-icons.delivering {
    color: #43b02a;
  }
  .material-icons.alert {
    color: #DA291C;
  }
}
</style>
