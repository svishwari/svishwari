<template>
  <div class="error-state-wrap text-center">
    <icon :type="iconType" :size="iconSize" />
    <div class="text-h2">{{ title }}</div>
    <div class="text-body-2 my-3">
      {{ subtitle }}
    </div>
  </div>
</template>

<script>
import Icon from "@/components/common/Icon"

export default {
  name: "Error",

  components: {
    Icon,
  },

  props: {
    title: {
      type: String,
      required: true,
    },
    subtitle: {
      type: String,
      required: true,
    },
    iconType: {
      type: String,
      required: true,
      default: 'destinations-null',
    },
    iconSize: {
      type: Number,
      required: false,
      default: 50,
    },
  },
}
</script>

<style lang="scss" scoped>
.error-state-wrap {
  background-color: var(--v-white-base);
  min-height: 280px;
  padding: 75px 0px 75px 0px;
}
</style>
