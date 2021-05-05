<template>
  <v-container fluid class="login-wrap">
    <v-row no-gutters>
      <v-col cols="6" class="left-section">
        <span class="overlay"></span>
      </v-col>
      <v-col cols="6" class="right-section">
        <Logo />
        <h1 class="font-weight-light">
          Access your <span class="altcolor">360&deg;</span> view
        </h1>
        <p>Jump right in where you left off, and leave the hard work on us!</p>
        <div class="login-form">
          <v-form ref="form" v-model="isFormValid">
            <TextField
              v-model="username"
              placeholderText="Enter Username"
              labelText="Username"
              backgroundColor="white"
              v-bind:required="true"
            ></TextField>
            <TextField
              v-model="password"
              placeholderText="Enter Password"
              labelText="Password"
              v-bind:appendIcon="toggleShowPassword ? 'mdi-eye' : 'mdi-eye-off'"
              v-bind:rules="[rules.required]"
              v-bind:InputType="toggleShowPassword ? 'text' : 'password'"
              @clickAppend="toggleShowPassword = !toggleShowPassword"
              backgroundColor="white"
              v-bind:required="true"
            ></TextField>

            <div v-if="loginFailed" class="error">
              Uh-oh, your email and password don’t match.
            </div>

            <router-link
              @click.native="forgotUsername"
              to="#"
              class="link-button font-weight-regular"
            >
              Forgot Username?
            </router-link>
            <router-link
              @click.native="forgotPassword"
              to="#"
              class="link-button font-weight-regular"
            >
              Forgot Password?
            </router-link>

            <!-- disable if form is not valid -->
            <huxButton
              v-bind:isDisabled="!isFormValid"
              size="large"
              ButtonText="Login"
              variant="tertiary"
              class="ml-0 mt-4 loginBtn"
              @click.native="initiateLogin()"
            ></huxButton>
          </v-form>
        </div>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import Logo from "../assets/images/logo.svg"
import auth from "@/auth"
import TextField from "@/components/common/TextField"
import huxButton from "@/components/common/huxButton"
export default {
  name: "Login",
  data() {
    return {
      username: "",
      password: "",
      toggleShowPassword: false,
      loginFailed: false,
      isFormValid: false,
      rules: {
        required: (value) => !!value || "Required.",
        min: (v) => v.length >= 8 || "Min 8 characters",
      },
    }
  },
  components: {
    Logo,
    TextField,
    huxButton,
  },
  methods: {
    initiateLogin() {
      auth.login(this.username, this.password, (loggedIn) => {
        if (!loggedIn) {
          this.loginFailed = true
        } else {
          this.$router.replace(this.$route.query.redirect || "/overview")
        }
      })
    },
    forgotUsername() {},
    forgotPassword() {},
  },
}
</script>

<style lang="scss" scoped>
.login-wrap {
  padding: 0;
  background: #e5e5e5;
  .left-section {
    height: 100vh;
    position: relative;
    background-size: cover;
    background-image: url("../assets/images/logon_background.png");
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
    p {
      font-family: "Open Sans";
      font-style: normal;
      font-weight: normal;
      font-size: 14px;
      line-height: 22px;
      color: #757b7b;
      margin-bottom: 20px;
    }
    .error {
      font-family: "Open Sans";
      font-style: normal;
      font-weight: normal;
      font-size: 10px;
      line-height: 14px;
      color: var(--v-error-base);
      margin-top: -15px;
    }
    .link-button {
      display: block;
      margin-top: 17px;
      text-decoration: none;
    }
    .loginBtn {
      margin-top: 30px;
      background-color: #ececec;
      width: 89px;
      height: 40px;
    }
  }
}
</style>
