<template>
  <div class="error-wrap">
    <div class="ta-center">
      <icon type="503-part1" size="120" color="black" class="align-left" />
      <icon type="503-part2" size="80" color="black" class="align-top" />
      <div class="error-code-font my-3">503</div>
      <div class="text-h1 mt-1">Unexpected service error occured.</div>
      <div class="ta-center text-h3 mt-2">
        This service is temporarily unavailable. Apologies for the<br />
        inconveniences this might mean to you. Thank you for your patience!
      </div>
      <huxButton
        variant="primary base"
        size="small"
        is-tile
        class="mt-14 px-6"
        data-e2e="go-prev-page"
        @click="goBack()"
      >
        Return to previous page
      </huxButton>
    </div>
  </div>
</template>

<script>
import Icon from "@/components/common/Icon.vue"
import huxButton from "@/components/common/huxButton"

export default {
  name: "ServiceError",

  components: {
    Icon,
    huxButton,
  },

  methods: {
    goBack() {
      this.$router.go(-1)
    },
  },
}
</script>

<style lang="scss" scoped>
.error-wrap {
  height: 100vh;
  display: flex;
  background: var(--v-white-base);
  justify-content: center;
  align-items: center;
  .align-left {
    margin-left: 79px !important;
  }
  .align-top {
    margin-bottom: 79px !important;
  }
}
</style>
