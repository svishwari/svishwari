<template>
  <v-container fluid class="login-wrap pa-0">
    <v-row no-gutters>
      <v-col cols="6" class="left-section">
        <span class="overlay"></span>
      </v-col>
      <v-col cols="6" class="right-section">
        <logo />
        <h1 class="text-h4 font-weight-regular">
          Access your <span class="altcolor">360&deg;</span> view
        </h1>
        <p class="font-weight-regular">
          Jump right in where you left off, and leave the hard work on us!
        </p>
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
  background: var(--v-primary-lighten1);
  .left-section {
    height: 100vh;
    position: relative;
    background-size: cover;
    background-image: url("../assets/images/logon_background.png");
    .overlay {
      background: var(--v-pink-base);
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
      font-family: "Open Sans" !important;
      font-weight: 300 !important;
      font-size: 24px !important;
      margin-top: 30px;
      line-height: 43px;
      color: var(--v-black-darken2);
      .altcolor {
        color: var(--v-pinkLittleDark-base);
      }
    }
    p {
      font-size: 14px !important;
      line-height: 22px;
      color: var(--v-black-darken1);
      margin-bottom: 20px;
    }
    .login-form {
      #okta-signin-container {
        ::v-deep .auth-container {
          font-family: "Open Sans", sans-serif !important;
          border: 0;
          margin: 0;
          background: transparent;
          width: 100%;
          padding-left: 5px;
          .okta-sign-in-header {
            display: none;
          }
          .auth-content {
            padding-left: 0;
            border: none;
            .icon {
              visibility: hidden;
            }
            .okta-form-title {
              display: none;
            }
            .o-form-label {
              label {
                font-family: Open Sans;
                font-style: normal;
                font-weight: normal;
                font-size: 12px;
                line-height: 16px;
                color: var(--v-black-darken4);
              }
            }
            .o-form-input {
              &.o-form-has-errors {
                .okta-form-input-error {
                  font-family: Open Sans;
                  font-style: normal;
                  font-weight: normal;
                  font-size: 12px;
                  line-height: 16px;
                  padding-top: 4px;
                  padding-left: 0;
                }
              }
            }
            .okta-form-input-field {
              border: none;
              background: transparent;
              input {
                padding: 10px 16px;
                background: var(--v-white-base);
                border: 1px solid var(--v-black-lighten3);
                box-sizing: border-box;
                border-radius: 4px;
              }
              &.o-form-has-errors {
                input {
                  border-color: var(--v-error-base);
                }
                .okta-form-input-error {
                  padding-left: 5px;
                }
              }
              &.focused-input {
                box-shadow: 0 0 8px var(--v-darkBlue-base);
              }
            }
            .o-form-button-bar {
              width: 90px;
              input {
                font-family: "Open Sans", sans-serif !important;
                width: 90px;
                height: 40px;
                box-sizing: border-box;
                background: var(--v-primary-base);
                box-shadow: 0px 1px 5px rgba(0, 0, 0, 0.25);
                content: "Log in";
              }
            }
          }
          .auth-footer {
            display: none;
          }
        }
      }
    }
  }
}
</style>
