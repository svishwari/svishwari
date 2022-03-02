<template>
  <div class="error-wrap">
    <div class="ta-center">
      <icon type="404" color="black" />
      <div class="fs-56">404</div>
      <div class="text-h1 mt-4">Uh oh we’ve lost this page.</div>
      <div class="ta-center text-h3 mt-2">
        Sorry about that. The reason we don’t find this page:
      </div>
      <span class="text-h3 ml-17 ta-left">
        &bull; the page has moved<br />
        &bull; the page no longer exist<br />
        &bull; you got distracted and made the typo in the address<br />
        &bull; you like visiting 404 pages and actually wanted to be here<br />
      </span>
      <v-btn
        :to="{ name: 'Home' }"
        data-e2e="launch"
        elevation="2"
        small
        tile
        class="btn-launch"
        color="primary"
      >
        Launch Hux
      </v-btn>
    </div>
  </div>
</template>

<script>
import Icon from "@/components/common/Icon.vue"

export default {
  name: "NotFound",

  components: {
    Icon,
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
  svg {
    min-width: 150px;
    min-height: 150px;
    width: 150px;
    height: 150px;
  }
  .fs-56 {
    font-size: 56px;
    line-height: 76px;
    font-weight: 300;
  }
  span {
    line-height: 31px;
    display: flex;
    align-items: flex-start;
    margin-top: 5px;
  }
  .btn-launch {
    min-height: 40px;
    min-width: 142px;
    font-size: 16px;
    margin-top: 45px;
  }
}
</style>
