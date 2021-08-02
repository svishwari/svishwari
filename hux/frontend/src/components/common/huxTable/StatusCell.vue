<template>
  <div class="status-wrapper">
    <v-icon v-if="cellValue == 'Active'" class="material-icons delivered">
      mdi-checkbox-blank-circle
    </v-icon>
    <huxButton
      v-if="cellValue == 'Delivering'"
      class="ma-0"
      is-outlined
      size="small"
      variant="successs"
      width="20"
      height="20"
      icon-type
    ></huxButton>
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
import huxButton from "@/components/common/huxButton"

export default Vue.extend({
  name: "StatusCell",
  components: {
    huxButton,
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
  },
})
</script>
<style lang="scss" scoped>
.status-wrapper {
  .material-icons.delivered {
    color: var(--v-success-lighten1);
  }
  .material-icons.delivering {
    color: var(--v-success-lighten2);
  }
  .material-icons.alert {
    color: var(--v-error-base);
  }
}
</style>
