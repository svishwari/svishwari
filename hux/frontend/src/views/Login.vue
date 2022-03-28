<template>
  <v-container fluid class="login-wrap pa-0">
    <v-row no-gutters>
      <v-col cols="6" class="left-section">
        <span class="overlay"></span>
      </v-col>
      <v-col cols="6" class="right-section">
        <logo />
        <h1>Access your <span class="altcolor">360&deg;</span> view</h1>
        <p class="body-1">
          Jump right in where you left off, and leave the hard work to us!
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
        authParams: {
          pkce: true,
          issuer: config.default.oidc.issuer,
          display: "page",
          scopes: ["openid", "email", "profile", "groups"],
        },
        features: {
          showPasswordToggleOnSignInPage: true,
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
    padding-top: 5% !important;
    padding-right: 6% !important;
    svg {
      width: 95px;
      height: 95px;
    }
    h1 {
      font-size: 28px;
      line-height: 40px;
      font-weight: 300 !important;
      margin-top: 30px;
      color: #333333;
      .altcolor {
        color: var(--v-pink-base);
      }
    }
    p {
      color: var(--v-black-lighten4);
      margin-bottom: 13px;
    }
    .login-form {
      #okta-signin-container {
        ::v-deep .auth-container {
          font-family: "Open Sans" !important;
          border: 0;
          margin: 0;
          background: transparent;
          width: 100%;
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
            .o-form-label-top {
              &:first-child {
                .o-form-label {
                  padding: 6px 0px 2px 5px !important;
                }
              }
              .o-form-label {
                padding: 12px 0px 2px 5px !important;
                label {
                  font-style: normal;
                  font-weight: normal;
                  font-size: 14px;
                  line-height: 16px;
                  color: var(--v-black-base);
                }
              }
            }
            .o-form-control {
              input {
                font-style: normal;
                font-weight: normal;
                font-size: 16px;
                line-height: 22px;
              }
            }
            .o-form-content {
              padding-bottom: 24px !important;
            }
            .o-form-input-name-remember {
              input {
                top: 2px;
                height: 18px;
                width: 18px;
              }
              label {
                font-style: normal;
                font-weight: normal;
                font-size: 16px;
                line-height: 16px;
              }
              .custom-checkbox {
                box-shadow: none;
              }
            }
            .email-button {
              background: var(--v-primary-base) !important;
            }
            .password-reset-email-sent {
              .o-form {
                .o-form-content {
                  p {
                    font-style: normal;
                    font-weight: normal;
                    font-size: 12px;
                    line-height: 16px;
                    color: var(--v-black-lighten4) !important;
                    margin-top: 6px !important;
                    margin-bottom: 16px !important;
                  }
                  .o-form-fieldset-container {
                    .button {
                      background: var(--v-primary-base) !important;
                    }
                  }
                }
              }
            }
            .o-form-input {
              &.o-form-has-errors {
                .okta-form-input-error {
                  padding-top: 4px;
                  padding-left: 0;
                }
              }
              .o-form-input-name-password {
                .password-toggle {
                  .visibility-16:before {
                    content: "\e0c3";
                    color: var(--v-black-base) !important;
                  }
                  .visibility-off-16:before {
                    content: "\e022";
                    color: var(--v-black-base) !important;
                  }
                }
              }
            }
            .okta-form-input-field {
              border: none;
              background: transparent;
              input {
                padding: 9px 16px;
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
              width: 107px;
              input {
                font-family: "Open Sans" !important;
                height: 40px;
                box-sizing: border-box;
                background: var(--v-primary-base);
                box-shadow: 0px 1px 5px rgba(0, 0, 0, 0.25);
              }
            }
          }
          .auth-footer {
            padding-top: 7px !important;
            font-style: normal;
            font-weight: normal;
            font-size: 16px;
            line-height: 22px;
            .link {
              &.help {
                box-shadow: none !important;
                color: var(--v-black-lighten4);
                &.js-help {
                  display: none;
                }
                &.js-back {
                  position: relative;
                  bottom: 21px !important;
                }
              }
            }
            #help-links-container {
              margin-top: -15px !important;
              display: block !important;
            }
          }
        }
      }
    }
  }
}
</style>
