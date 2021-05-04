<template>
  <v-card
    class="text-center rounded-lg"
    min-width="220px"
    max-width="260px"
    :disabled="!active"
    :to="to"
    @click="$emit('click')"
  >
    <v-btn fab :ripple="false" elevation="2" color="tertiary" class="mt-4">
      <v-icon color="primary" x-large>
        {{ icon }}
      </v-icon>
    </v-btn>
    <v-card-title class="justify-center primary--text">
      {{ title }}
    </v-card-title>
    <v-card-subtitle>
      {{ description }}
    </v-card-subtitle>
  </v-card>
</template>

<script>
export default {
  name: "card-info",

  props: {
    icon: {
      type: String,
      required: false,
      default: "mdi-plus",
    },

    title: {
      type: String,
      required: false,
      default: "Info card title",
    },

    description: {
      type: String,
      required: false,
      default: "Info card description",
    },

    active: {
      type: Boolean,
      required: false,
      default: true,
    },

    to: {
      type: String,
      required: false,
    },
  },
}
</script>
