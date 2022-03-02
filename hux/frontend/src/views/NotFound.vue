<template>
  <div class="error-wrap">
    <div class="ta-center">
      <icon :type="404" :size="150" color="black" />
      <div class="fs-56">404</div>
      <div class="text-h1 mt-4">Uh oh we’ve lost this page.</div>
      <div class="ta-center text-h3 mt-2">
        Sorry about that. The reason we don’t find this page:
      </div>
      <div class="text-h3 ml-17 ta-left mt-1 gap">
        &bull; the page has moved<br />
        &bull; the page no longer exist<br />
        &bull; you got distracted and made the typo in the address<br />
        &bull; you like visiting 404 pages and actually wanted to be here<br />
      </div>
      <huxButton
        variant="primary base"
        size="small"
        is-tile
        class="btn-launch text-button mt-12"
        data-e2e="launch"
        @click="launch"
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
    launch: function () {
      this.$router.push({
        name: "Home",
      })
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
  .fs-56 {
    font-size: 56px;
    line-height: 76px;
    font-weight: 300;
  }
  .gap {
    line-height: 31px;
    display: flex;
    align-items: flex-start;
  }
}
</style>
