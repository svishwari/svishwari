import { OktaAuth } from "@okta/okta-auth-js";
const config = require("@/config");
import store from './store/index';

const authClient = new OktaAuth({ issuer: config.default.oidc.issuer })

export default {
  login(email, pass, cb) {
    cb = arguments[arguments.length - 1]
    if (localStorage.token) {
      if (cb) cb(true)
      this.onChange(true)
      return
    }
    return authClient
      .signInWithCredentials({
        username: email,
        password: pass,
      })
      .then((transaction) => {
        if (transaction.status === "SUCCESS") {
          return authClient.token
            .getWithoutPrompt({
              clientId: config.default.oidc.clientId,
              responseType: ["id_token", "token"],
              scopes: ["openid", "email", "profile"],
              sessionToken: transaction.sessionToken,
              redirectUri: window.location.origin + "/login/callback",
            })
            .then((response) => {
              store.commit('SET_USER_NAME', transaction.user.profile)
              console.log(store.state);
              localStorage.token = response.tokens.accessToken.value;
              localStorage.idToken = response.tokens.idToken.value;
              localStorage.firstName = transaction.user.profile.firstName;
              // localStorage.firstName = store.state.userName.firstName;
              localStorage.lastName = transaction.user.profile.lastName;
              // localStorage.lastName = store.state.userName.lastName;
              if (cb) cb(true);
              this.onChange(true);
            });
        }
      })
      .catch((err) => {
        console.error(err.message)
        if (cb) cb(false)
        this.onChange(false)
      })
  },

  getToken() {
    return localStorage.token
  },

  logout(cb) {
    delete localStorage.token
    delete localStorage.idToken
    if (cb) cb()
    this.onChange(false)
    return authClient.signOut()
  },

  loggedIn() {
    return !!localStorage.token
  },

  onChange() {},
}
