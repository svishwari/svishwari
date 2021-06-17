<template>
  <tooltip>
    <template slot="label-content">
      <span class="neroBlack--text">
        {{ Value | Numeric(false, false, true) | Empty }}
      </span>
    </template>
    <template slot="hover-content">
      {{ Value | Numeric(true) | Empty }}
    </template>
  </tooltip>
</template>
<script>
import Vue from "vue"
import Tooltip from "../Tooltip.vue"
export default Vue.extend({
  components: { Tooltip },
  name: "size",
  props: {
    value: {
      type: Number,
      required: true,
    },
  },
  computed: {
    Value() {
      return this.value ? this.value : 0
    },
  },
})
</script>
