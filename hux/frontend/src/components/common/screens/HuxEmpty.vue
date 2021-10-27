<template>
  <div ref="emptyState" class="empty-state-wrap">
    <div v-for="index in boxCount" :key="index" class="box"></div>
    <div class="text-center">
      <icon
        :type="iconType"
        :size="iconSize"
        color="primary"
        variant="lighten6"
      />
      <div class="text-h2">{{ title }}</div>
      <div class="text-body-2 my-3">
        {{ subtitle }}
      </div>
      <slot name="button"></slot>
    </div>
  </div>
</template>

<script>
import Icon from "@/components/common/Icon"

export default {
  name: "HuxEmpty",

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

  data() {
    return {
      width: null,
      height: null,
      boxCount: 0,
    }
  },

  mounted() {
    this.width = this.$refs.emptyState && this.$refs.emptyState.clientWidth
    this.height = this.$refs.emptyState && this.$refs.emptyState.clientHeight
    this.boxCount = Math.round((this.width * this.height) / (125 * 125))
  },
}
</script>

<style lang="scss" scoped>
.empty-state-wrap {
  height: 464px;
  overflow: hidden;
  padding: 36px 30px 36px 30px;
  position: relative;
  .text-center {
    margin: 0;
    position: absolute;
    top: 200px;
    left: 50%;
    transform: translate(-50%, -50%);
    z-index: 2;
  }
  .box {
    width: 125px;
    height: 125px;
    margin: 8px 20px 8px 20px;
    background-color: white;
    position: relative;
    top: 0;
    left: 0;
    float: left;
    border-radius: 12px;
  }
}
</style>
