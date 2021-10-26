<template>
  <div class="empty-state-wrap" ref="emptyState">
    <div class="box" v-for="index in boxCount" :key="index"></div>
    <div class="text-center">
      <icon :type="iconType" :size="iconSize" color="primary" variant="lighten6" />
      <div class="text-h2">{{ title }}</div>
      <div class="text-body-2 my-3">
        {{ subtitle }}
      </div>
      <hux-button
        variant="primary"
        is-tile
        width="224"
        height="40"
        class="text-button my-4"
      >
        Request a data source
      </hux-button>
    </div>
  </div>
</template>

<script>
import Icon from "@/components/common/Icon"
import HuxButton from "@/components/common/huxButton"

export default {
  name: "Empty",

  components: {
    Icon,
    HuxButton,
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
    z-index: 100;
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
