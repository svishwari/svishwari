<template>
  <v-hover>
    <template #default="{ hover }">
      <v-card
        class="text-center rounded-lg card-info-wrapper card-shadow pa-3"
        min-width="220px"
        max-width="260px"
        :disabled="!active"
        :to="to"
        :elevation="hover ? 10 : 0"
        :hover="true"
        :outlined="!active"
        @click="$emit('click')"
      >
        <v-btn
          fab
          :ripple="false"
          elevation="0"
          :outlined="active"
          color="black lighten-2"
          class="mt-4"
        >
          <v-icon :color="active ? 'primary' : 'white'" x-large>
            {{ icon }}
          </v-icon>
        </v-btn>
        <v-card-title
          class="justify-center font-weight-regular"
          :class="{ 'primary--text': active }"
          data-e2e="card-title"
        >
          {{ title }}
        </v-card-title>
        <v-card-subtitle
          data-e2e="card-description"
          :class="{ 'black--text text--darken-4': active }"
        >
          {{ description }}
        </v-card-subtitle>
      </v-card>
    </template>
  </v-hover>
</template>

<script>
export default {
  name: "CardInfo",

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
      type: Object,
      required: false,
    },
  },
}
</script>
<style lang="scss" scoped>
.card-info-wrapper {
  .v-card__title {
    margin-bottom: 10px;
  }
}
</style>
