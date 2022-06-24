<template>
  <v-card class="pa-6 pt-5" :width="getWidth">
    <div class="mb-4">
      <div class="card-header" :class="$slots.filters ? 'mb-2' : ''">
        <div class="title-bar">
          <icon 
            v-if="iconType"
            :type="iconType"
            :size="24"
            :color="iconColor"
            outline
            :borderColor="borderColor"
            :bgColor="iconBgColor"
            class="mr-1"
          />
          <span class="text-h4">{{ title }}</span>
        </div>
        <slot name="call-to-action"></slot>
      </div>
      <slot name="filters" class="filters-bar"></slot>
    </div>
    <slot name="body"></slot>
  </v-card>
</template>

<script>
import Icon from "../icons/Icon2.vue"

export default {
  name: "PlainCard",
  components: { Icon },
  props: {
    iconType: {
      type: String,
      required: false,
    },
    iconColor: {
      type: String,
      required: false,
      default: "primary-base",
    },
    iconBorderColor: {
      type: String,
      required: false,
      default: "primary-base",
    },
    iconBgColor: {
      type: String,
      required: false,
      default: "white-base",
    },
    title: {
      type: String,
      required: true,
    },
    size: {
      type: String,
      required: false,
      default: "small",
    },
  },

  computed: {
    getWidth() {
      return this.size == "small" ? 368 : this.size == "medium" ? 564 : 1152
    },
  },
}
</script>

<style lang="scss" scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  height: 24px;
}
.filters-bar {
  padding-left: -24px;
  padding-right: -24px;
}
.title-bar {
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>
