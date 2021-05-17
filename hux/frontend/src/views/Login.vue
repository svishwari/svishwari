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
          <div id="okta-signin-container" class="okta-container"></div>
        </div>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import Logo from "../assets/images/logo.svg"
import OktaSignIn from "@okta/okta-signin-widget"
import "@okta/okta-signin-widget/dist/css/okta-sign-in.min.css"
const config = require("@/config")

export default {
  name: "Login",
  components: {
    Logo,
  },
  mounted: function () {
    this.$nextTick(function () {
      this.widget = new OktaSignIn({
        baseUrl: config.default.oidc.issuer.split("/oauth2")[0],
        clientId: config.default.oidc.clientId,
        redirectUri: window.location.origin + "/login/callback",
        logo: require("@/assets/images/logo.png"),
        language: "en",
        i18n: {
          en: {
            "primaryauth.title": "Login | HUX Unified UI",
          },
        },
        authParams: {
          pkce: true,
          issuer: config.default.oidc.issuer,
          display: "page",
          scopes: ["openid", "email", "profile"],
        },
      })

      this.widget.renderEl(
        { el: "#okta-signin-container" },
        () => {},
        (err) => {
          throw err
        }
      )
    })
  },
  destroyed() {
    // Remove the widget from the DOM on path change
    this.widget.remove()
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
    .login-form {
      #okta-signin-container {
        ::v-deep .auth-container {
          margin: 0;
          background: transparent;
          .okta-sign-in-header {
            display: none;
          }
          .auth-content {
            padding-left: 0;
            border: none;
            .okta-form-title {
              display: none;
            }
          }
        }
      }
    }
  }
}
</style>
