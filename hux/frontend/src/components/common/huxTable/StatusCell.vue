<template>
  <div class="status-wrapper">
    <v-icon v-if="cellValue == 'Active'" class="material-icons delivered">
      mdi-checkbox-blank-circle
    </v-icon>
    <huxButton class="ma-0" v-if="cellValue == 'Delivering'"
      v-bind:isOutlined="true"
      size="small"
      variant="#43b02a"
      width="20"
      height="20"
      v-bind:iconType="true"
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
    color: #43b02a;
  }
  .material-icons.delivering {
    color: #43b02a;
  }
  .material-icons.alert {
    color: #da291c;
  }
}
</style>
