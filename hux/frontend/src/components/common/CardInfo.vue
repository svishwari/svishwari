<template>
  <v-hover>
    <template v-slot:default="{ hover }">
      <v-card
        class="text-center rounded-lg"
        min-width="220px"
        max-width="260px"
        :disabled="!active"
        :to="{ name: to }"
        @click="$emit('click')"
        :elevation="hover ? 10 : 0"
        :hover="true"
        :outlined="!active"
      >
        <v-btn fab :ripple="false" elevation="0" outlined color="zircon" class="mt-4">
          <v-icon color="primary" x-large>
            {{ icon }}
          </v-icon>
        </v-btn>
        <v-card-title class="justify-center font-weight-regular" v-bind:class="{ 'primary--text': active }">
          {{ title }}
        </v-card-title>
        <v-card-subtitle v-bind:class="{ 'neroBlack--text': active }">
          {{ description }}
        </v-card-subtitle>
      </v-card>
    </template>
  </v-hover>
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
