<template>
  <v-menu bottom offset-y open-on-hover class="cursor-default">
    <template v-slot:activator="{ on, attrs }">
      <span v-bind="attrs" v-on="on" class="cursor-default">
        {{ value | Date("relative") | Empty }}
      </span>
    </template>
    <v-list>
      <v-list-item>
        <v-list-item-title class="neroBlack--text">
          {{ value | Date | Empty }}
        </v-list-item-title>
      </v-list-item>
    </v-list>
  </v-menu>
</template>
<script>
import Vue from "vue"
export default Vue.extend({
  name: "TimeStamp",
  props: {
    value: {
      type: String,
      required: true,
    },
  },
})
</script>
