<template>
  <div class="not-found-wrap">
    <div class="ta-center">
      <logo />
      <div class="text-h1 mt-12">
        It looks like you do not have access to Hux
      </div>
      <div class="ta-center text-h3 mt-2">
        It’s an easy fix, though. Leave your email address below and we will get
        back to you shortly.<br />
        Thank you for your patience!
      </div>
      <v-row class="ma-0 mt-14 pa-0 center">
        <div class="text-decoration-none">
          <huxButton
            variant="primary base"
            size="small"
            :box-shadow="false"
            is-tile
            class="mt-5 px-6 mx-2 box-shadow-25-light"
            data-e2e="request-access"
            @click="mappingRoute('access')"
          >
            Request access
          </huxButton>
        </div>
        <div class="text-decoration-none">
          <huxButton
            variant="white"
            icon-color="primary"
            size="small"
            :box-shadow="false"
            is-tile
            class="mt-5 px-6 primary--text box-shadow-25-light"
            data-e2e="back-to-previous-page"
            @click="mappingRoute('previous')"
          >
            Return to previous page
          </huxButton>
        </div>
      </v-row>
    </div>
  </div>
</template>

<script>
import Logo from "@/assets/images/logo.svg"
import huxButton from "@/components/common/huxButton"

export default {
  name: "NoAccessUserLogin",

  components: {
    huxButton,
    Logo,
  },

  data() {
    return {
      email: "",
    }
  },

  methods: {
    mappingRoute(val) {
      if (val == "access") {
        this.$router.push({ path: "/" })
      } else if (val == "previous") {
        this.$router.go(-2)
      }
    },
  },
}
</script>

<style lang="scss" scoped>
.not-found-wrap {
  height: 100vh;
  display: flex;
  background: var(--v-white-base);
  justify-content: center;
  align-items: center;
  .ta-center {
    svg {
      min-width: 140px;
      min-height: 140px;
      width: 140px;
      height: 140px;
    }
    ::v-deep .text-field-hux {
      margin-top: 2px !important;
      label {
        margin-bottom: 2px !important;
      }
    }
  }
}
</style>
