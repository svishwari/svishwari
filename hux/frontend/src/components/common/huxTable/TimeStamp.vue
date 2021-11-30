<template>
  <tooltip>
    <template slot="label-content">
      {{ value | Date("relative") | Empty }}
    </template>
    <template slot="hover-content">
      <span class="text-body-2 black--text">
        {{ value | Date | Empty }}
      </span>
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
