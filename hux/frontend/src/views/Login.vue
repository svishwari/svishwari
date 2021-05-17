<template>
  <div class="login">
    <div id="okta-signin-container"></div>
  </div>
</template>

<script>
import OktaSignIn from "@okta/okta-signin-widget"
import "@okta/okta-signin-widget/dist/css/okta-sign-in.min.css"
const config = require("@/config")

export default {
  name: "Login",
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
