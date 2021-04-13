<template>
  <v-container fluid class="login-wrap">
    <v-row no-gutters>
      <v-col
        cols="6"
        :style="{
          'background-image':
            'url(' + require('../assets/images/logon_background.png') + ')',
        }"
        class="left-section"
      >
        <span class="overlay"></span>
      </v-col>
      <v-col cols="6" class="right-section">
        <Logo />
        <h1>Access your <span class="altcolor">360°</span> view</h1>
        <pre>
 Jump right in where you left off, and leave the hard work on us!</pre
        >
        <div class="login-form">
          <v-form ref="form" v-model="isFormValid" lazy-validation>
            <v-text-field
              v-model="username"
              label="Username"
              autocomplete="username"
              required
            ></v-text-field>
            <v-text-field
              v-model="password"
              :append-icon="show1 ? 'mdi-eye' : 'mdi-eye-off'"
              :rules="[rules.required]"
              :type="show1 ? 'text' : 'password'"
              name="input-10-1"
              label="Password"
              autocomplete="newPassword"
              @click:append="show1 = !show1"
            ></v-text-field>
            <div v-if="loginFailed" class="error">
              Uh-oh, your email and password don’t match.
            </div>

            <router-link
              @click.native="forgotUsername"
              to="#"
              class="link-button"
              >Forgot Username?</router-link
            >
            <router-link
              @click.native="forgotPassword"
              to="#"
              class="link-button"
              >Forgot Password?</router-link
            >

            <!-- disable if form is not valid -->
            <v-btn
              :disabled="!isFormValid"
              x-large
              class="mt-4"
              @click="initiateLogin()"
              >Login</v-btn
            >
          </v-form>
        </div>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import Logo from "../assets/images/logo.svg";
import auth from "./auth/auth";
export default {
  name: "Login",
  data() {
    return {
      username: "",
      password: "",
      show1: false,
      loginFailed: false,
      isFormValid: false,
      rules: {
        required: (value) => !!value || "Required.",
        min: (v) => v.length >= 8 || "Min 8 characters",
      },
    };
  },
  components: {
    Logo,
  },
  methods: {
    initiateLogin() {
      auth.login(this.username, this.password, (loggedIn) => {
        if (!loggedIn) {
          this.loginFailed = true;
        } else {
          this.$router.replace(this.$route.query.redirect || "/home");
        }
      });
    },
    forgotUsername() {},
    forgotPassword() {},
  },
};
</script>

<style lang="scss" scoped>
.login-wrap {
  padding: 0;
  background: #e5e5e5;
  .left-section {
    height: 100vh;
    position: relative;
    background-size: cover;
    .overlay {
      background: #b54acf;
      opacity: 0.3;
      position: absolute;
      top: 0px;
      z-index: 3;
      height: 100%;
      width: 100%;
    }
  }
  .right-section {
    padding-left: 7% !important;
    padding-top: 6% !important;
    padding-right: 6% !important;
    svg {
      width: 95px;
      height: 95px;
    }
    h1 {
      margin-top: 30px;
      font-style: normal;
      font-weight: 600;
      font-size: 24px;
      line-height: 43px;
      color: #333333;
      .altcolor {
        color: #f03bc8;
      }
    }
    pre {
      font-family: Open Sans;
      font-style: normal;
      font-weight: normal;
      font-size: 14px;
      line-height: 22px;
      color: #757b7b;
    }
    .error {
      font-family: Open Sans;
      font-style: normal;
      font-weight: normal;
      font-size: 10px;
      line-height: 14px;
      color: #da291c;
      margin-top: -15px;
    }
    .link-button {
      display: block;
      margin-top: 17px;
    }
  }
}
</style>
