<template>
  <tooltip>
    <template #label-content>
      <span
        class="blue-grey d-flex align-center justify-center"
        :style="{ 'border-color': getColorCode(localName) }"
      >
        {{ localName | shortName }}
      </span>
    </template>
    <template #hover-content>
      {{ localName }}
    </template>
  </tooltip>
</template>

<script>
import { generateColor } from "@/utils"
import Tooltip from "@/components/common/Tooltip.vue"

const DEFAULT_NAME = "Sarah Huxly"

export default {
  name: "Avatar",

  components: {
    Tooltip,
  },

  props: {
    name: {
      type: String,
      required: false,
    },
  },

  computed: {
    localName() {
      return this.name || DEFAULT_NAME
    },
  },

  methods: {
    getColorCode(name) {
      return generateColor(name, 30, 60) + " !important"
    },
  },
}
</script>

<style lang="scss" scoped>
.blue-grey {
  display: inline-flex !important;
  border-width: 2px;
  border-style: solid;
  border-radius: 50%;
  font-size: 14px;
  width: 35px;
  height: 35px;
  line-height: 22px;
  color: var(--v-black-darken4) !important;
  cursor: default !important;
  background: transparent !important;
}
</style>
