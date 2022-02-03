<template>
  <tooltip>
    <template #label-content>
      <span
        class="blue-grey d-flex align-center justify-center text-body-1"
        :class="requested ? 'dashed-border' : ''"
        :style="{ 'border-color': getColorCode(localName) }"
      >
        <span :class="requested ? 'grey-color' : ''">{{
          localName | shortName
        }}</span>
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
    requested: {
      type: Boolean,
      required: false,
      default: false,
    },
  },

  computed: {
    localName() {
      return this.name || DEFAULT_NAME
    },
  },

  methods: {
    getColorCode(name) {
      if (this.requested) {
        return "#D0D0CE !important"
      }
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
  width: 35px;
  height: 35px;
  line-height: 22px;
  color: var(--v-black-darken4) !important;
  cursor: default !important;
  background: transparent !important;
}
.dashed-border {
  border-style: dashed !important;
}
.grey-color {
  font-style: italic;
  font-weight: normal;
  font-size: 16px;
  line-height: 22px;
  color: var(--v-black-lighten3);
}
</style>
