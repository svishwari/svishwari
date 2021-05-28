<template>
  <v-menu bottom offset-y open-on-hover class="cursor-default">
    <template v-slot:activator="{ on, attrs }">
      <span
        class="blue-grey d-flex align-center justify-center"
        v-bind="attrs"
        v-on="on"
        v-bind:style="{ 'border-color': userInfo.color }"
      >
        {{ userInfo.fullName | shortName }}
      </span>
    </template>
    <v-list>
      <v-list-item>
        <v-list-item-title>{{ userInfo.fullName }}</v-list-item-title>
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
  computed: {
    userInfo() {
      if (this.name) {
        return {
          shortName: this.name
            .split(" ")
            .map((n) => n[0])
            .join(""),
          fullName: this.name,
          color: this.getColorCode(this.name),
        }
      } else {
        return {
          shortName: "",
          fullName: "",
          color: "",
        }
      }
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
