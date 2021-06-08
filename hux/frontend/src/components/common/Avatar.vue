<template>
  <v-menu bottom offset-y open-on-hover class="cursor-default">
    <template v-slot:activator="{ on, attrs }">
      <span
        class="blue-grey d-flex align-center justify-center"
        v-bind="attrs"
        v-on="on"
        :style="{ 'border-color': getColorCode(name) }"
      >
        {{ name | shortName }}
      </span>
    </template>
    <v-list>
      <v-list-item>
        <v-list-item-title class="neroBlack--text">{{ name }}</v-list-item-title>
      </v-list-item>
    </v-list>
  </v-menu>
</template>

<script>
import { generateColor } from "@/utils"

export default {
  name: "Avatar",
  props: {
    name: {
      type: String,
      default: "",
      required: true,
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
  color: var(--v-neroBlack-base) !important;
  cursor: default !important;
  background: transparent !important;
}
</style>
