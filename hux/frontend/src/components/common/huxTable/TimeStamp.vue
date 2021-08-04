<template>
  <tooltip>
    <template slot="label-content">
      {{ value | Date("relative") | Empty }}
    </template>
    <template slot="hover-content">
      {{ value | Date | Empty }}
    </template>
  </tooltip>
</template>
<script>
import Vue from "vue"
import Tooltip from "../Tooltip.vue"
export default Vue.extend({
  name: "TimeStamp",
  components: {
    Tooltip,
  },
  props: {
    value: {
      type: String,
      required: false,
      default: "",
    },
  },
})
</script>
