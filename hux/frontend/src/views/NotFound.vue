<template>
  <div class="error-wrap">
    <div class="ta-center">
      <icon :type="404" :size="150" color="black" />
      <div class="error-code-font">404</div>
      <div class="text-h1 mt-4">Uh oh we’ve lost this page.</div>
      <div class="ta-center text-h3 mt-2 tab-404">
        Sorry about that. This error occurred because:
      </div>
      <div class="text-h3 ml-4 ta-left mt-1 gap">
        &bull;&nbsp; the page has moved<br />
        &bull;&nbsp; the page no longer exists<br />
        &bull;&nbsp; you got distracted and made the typo in the address<br />
        &bull;&nbsp; you like visiting 404 pages and actually want to be here
      </div>
      <huxButton
        variant="primary base"
        size="small"
        is-tile
        class="btn-launch text-button mt-12"
        data-e2e="launch"
        @click="launch()"
      >
        Launch Hux
      </huxButton>
    </div>
  </div>
</template>

<script>
import Icon from "@/components/common/Icon.vue"
import huxButton from "@/components/common/huxButton"

export default {
  name: "NotFound",

  components: {
    Icon,
    huxButton,
  },

  methods: {
    launch() {
      this.$router.back()
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
  .gap {
    line-height: 31px;
    display: flex;
    align-items: flex-start;
  }
  .tab-404 {
    margin-right: 92px;
  }
}
</style>
