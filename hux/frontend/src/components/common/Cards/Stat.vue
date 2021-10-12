<template>
  <v-menu
    bottom
    offset-y
    offset-x
    nudge-left="40px"
    nudge-top="10px"
    open-on-hover
  >
    <template #activator="{ on }">
      <div class="px-4 border-start border-zircon" :class="statClass" v-on="on">
        <h4 class="text-h4 mb-0">{{ value }}</h4>
        <div class="text-caption black--text text--darken-4">{{ label }}</div>
      </div>
    </template>
    <div v-if="$slots.default" class="px-4 py-3 text-caption white">
      <slot name="default" />
    </div>
  </v-menu>
</template>

<script>
export default {
  name: "Stat",

  props: {
    label: {
      type: String,
      required: false,
    },
    value: {
      type: String,
      required: false,
    },
    statClass: {
      type: String,
      required: false,
    },
  },
}
</script>
