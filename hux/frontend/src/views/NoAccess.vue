<template>
  <div class="not-found-wrap">
    <div class="ta-center">
      <logo />
      <div class="text-h1 mt-12">
        It looks like that you do not have access to Hux
      </div>
      <div class="ta-center text-h3 mt-2">
        It’s an easy fix, though. Leave your email address below and we will get
        back to you shortly.<br />
        Thank you for your patience!
      </div>
      <v-row class="ma-0 mt-14 pa-0">
        <v-col class="pa-0">
          <text-field
            v-model="email"
            label-text="Your email"
            placeholder-text="example@example.com"
            data-e2e="email"
            required
          ></text-field>
        </v-col>
        <router-link to="/" class="text-decoration-none">
          <huxButton
            variant="primary base"
            size="small"
            :box-shadow="false"
            is-tile
            class="mt-5 px-6 mx-2 box-shadow-25-light"
            data-e2e="request-access"
          >
            Request access
          </huxButton>
        </router-link>
        <router-link to="/login" class="text-decoration-none">
          <huxButton
            variant="white"
            icon-color="primary"
            size="small"
            :box-shadow="false"
            is-tile
            class="mt-5 px-6 primary--text box-shadow-25-light"
            data-e2e="back-to-login"
          >
            Return to login
          </huxButton>
        </router-link>
      </v-row>
    </div>
  </div>
</template>

<script>
import Logo from "@/assets/images/logo.svg"
import huxButton from "@/components/common/huxButton"
import TextField from "@/components/common/TextField.vue"

export default {
  name: "NoAccess",

  components: {
    huxButton,
    Logo,
    TextField,
  },

  data() {
    return {
      email: "",
    }
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
