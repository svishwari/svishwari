<template>
  <tooltip>
    <template #label-content>
      <span class="black--text text--darken-4">
        {{ Value | Numeric(false, false, true) | Empty }}
      </span>
    </template>
    <template #hover-content>
      {{ Value | Numeric(true) | Empty }}
    </template>
  </tooltip>
</template>
<script>
import Vue from "vue"
import Tooltip from "../Tooltip.vue"
export default Vue.extend({
  name: "Size",
  components: { Tooltip },
  props: {
    value: {
      type: Number,
      required: false,
      default: 0,
    },
  },
  computed: {
    Value() {
      return this.value ? this.value : 0
    },
  },
})
</script>
