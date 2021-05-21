<template>
  <v-menu bottom offset-y open-on-hover class="cursor-default">
    <template v-slot:activator="{ on, attrs }">
      <span v-bind="attrs" v-on="on" class="cursor-default">
        {{ cellValue.label | TitleCase }}
      </span>
    </template>
    <v-list>
      <v-list-item>
        <v-list-item-title>
          {{ cellValue.tooltip }}
        </v-list-item-title>
      </v-list-item>
    </v-list>
  </v-menu>
</template>
<script>
import moment from "moment"
import Vue from "vue"
export default Vue.extend({
  name: "DateTimeCell",
  data() {
    return {
      cellValue: null,
    }
  },
  beforeMount() {
    if (this.params.value) {
      this.cellValue = {
        label: moment(new Date(this.params.value)).fromNow(),
        tooltip: moment(new Date(this.params.value)).format("LLL"),
      }
    } else {
      this.cellValue = {
        label: "",
        tooltip: "",
      }
    }
  },
})
</script>
