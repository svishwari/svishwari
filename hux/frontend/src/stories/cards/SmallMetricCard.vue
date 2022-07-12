<template>
  <v-card class="pa-4 card-style" width="192">
    <div class="mb-1 card-header">
      <icon
        v-if="icon"
        :type="icon"
        size="14"
        color="primary"
        variant="base"
        class="mr-1 mt-1"
      />
      <span class="text-body-4">
        <a v-if="isLink">{{ title }}</a>
        <span v-else>{{ title }}</span>
      </span>
      <tooltip v-if="tooltipContent">
        <template #label-content>
          <icon
            type="informative-rev"
            :size="12"
            color="primary"
            variant="base"
            class="ml-3 mt-1"
          />
        </template>
        <template #hover-content>
          {{ tooltipContent }}
        </template>
      </tooltip>
    </div>
    <slot v-if="!isError" name="body"><div>-</div></slot>
    <div v-else>
      <icon type="error" :size="16" />
      <span class="error-text text-button">Error</span>
    </div>
  </v-card>
</template>

<script>
import icon from "../icons/Icon2.vue"
import Tooltip from "../tooltip/Tooltip2.vue"

export default {
  name: "SmallMetricCard",
  components: { icon, Tooltip },
  props: {
    icon: {
      type: String,
      required: false,
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
    tooltipContent: {
      type: String,
      required: false,
    },
    isError: {
      type: Boolean,
      required: false,
      default: false,
    },
    isLink: {
      type: Boolean,
      required: false,
      default: false,
    },
  },
}
</script>

<style lang="scss" scoped>
.card-style {
  border-radius: 12px;
}
.card-header {
  display: flex;
  height: 24px;
}
.error-text {
  color: red;
  margin-left: 4px;
}
</style>
