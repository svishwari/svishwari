<template>
  <v-menu bottom offset-y open-on-hover>
    <template v-slot:activator="{ on, attrs }">
      <span v-bind="attrs" v-on="on" class="cursor-default">
        {{ value | ApproxSize }}
      </span>
    </template>
    <v-list>
      <v-list-item>
        <v-list-item-title>{{ value | FormatSize }}</v-list-item-title>
      </v-list-item>
    </v-list>
  </v-menu>
</template>
<script>
import Vue from "vue"
export default Vue.extend({
  name: "size",
  props: {
    value: {
      type: Number,
      required: true,
    },
  },
})
</script>
