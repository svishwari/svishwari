<template>
  <v-menu bottom offset-y open-on-hover class="cursor-default">
    <template #activator="{ on, attrs }">
      <span
        class="blue-grey d-flex align-center justify-center"
        v-bind="attrs"
        :style="{ 'border-color': cellValue.color }"
        v-on="on"
      >
        {{ cellValue.shortName | TitleCase }}
      </span>
    </template>
    <v-list>
      <v-list-item>
        <v-list-item-title>{{
          cellValue.fullName | TitleCase
        }}</v-list-item-title>
      </v-list-item>
    </v-list>
  </v-menu>
</template>
<script>
import Vue from "vue"
import { generateColor } from "@/utils"
export default Vue.extend({
  name: "UserAvatarCell",
  data() {
    return {
      cellValue: null,
    }
  },
  beforeMount() {
    if (this.params.value) {
      const _fullName =
        this.params.value.first_name + " " + this.params.value.last_name
      this.cellValue = {
        shortName: _fullName
          .split(" ")
          .map((n) => n[0])
          .join(""),
        fullName: _fullName,
        color: generateColor(_fullName, 30, 60) + " !important",
      }
    } else {
      this.cellValue = {
        shortName: "",
        fullName: "",
        color: "",
      }
    }
  },
})
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
  color: var(--v-black-darken4) !important;
  cursor: default !important;
  background: transparent !important;
}
</style>
