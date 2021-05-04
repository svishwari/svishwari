<template>
  <v-card
    class="metric-card-wrapper"
    @click="$emit('click')"
    :disabled="!active"
    :width="width"
    :height="height"
    elevation="0"
  >
    <v-list-item three-line>
      <v-list-item-content>
        <v-list-item-title
          class="item-headline mt-1"
          v-bind:class="active ? 'primary--text ' : 'gray--text '"
        >
          {{ title }}
        </v-list-item-title>
        <v-list-item-subtitle class="item-subtitle mb-3 neroBlack--text">
          {{ subtitle }}
        </v-list-item-subtitle>
      </v-list-item-content>
      <v-icon color="zircon" x-large> {{ icon }} </v-icon>
    </v-list-item>
  </v-card>
</template>

<script>
export default {
  name: "metric-card",

  props: {
    icon: {
      type: String,
      required: false,
    },

    title: {
      type: String,
      required: false,
      default: "Info card title",
    },

    subtitle: {
      type: String,
      required: false,
      default: "Info card description",
    },

    active: {
      type: Boolean,
      required: false,
      default: true,
    },
    width: {
      type: Number,
      required: false,
      default: 135,
    },
    height: {
      type: Number,
      required: false,
      default: 80,
    },
  },
}
</script>

<style lang="scss" scoped>
.metric-card-wrapper {
  border: 1px solid #e2eaec;
  .item-headline {
    font-size: 12px;
  }
  .v-list-item__title {
    font-weight: 400;
  }
  &.v-card--disabled {
    background-color: unset;
    .v-list-item__title {
      color: #4f4f4f;
    }
  }
}
</style>
