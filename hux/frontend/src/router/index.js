import Vue from "vue"
import VueRouter from "vue-router"

import Auth from "@okta/okta-vue"
import { pageTitle } from "@/utils"
const config = require("@/config")

Vue.use(Auth, {
  issuer: config.default.oidc.issuer,
  clientId: config.default.oidc.clientId,
  redirectUri: window.location.origin + "/login/callback",
  scopes: ["openid", "profile", "email"],
  pkce: true,
})

Vue.use(VueRouter)

const NotFoundRoute = {
  path: "*",
  component: () => import("@/views/NotFound"),
  meta: {
    title: "Not Found",
    layout: "default",
  },
}

const routes = [
  {
    path: "/",
    name: "Welcome",
    component: () => import("@/views/Welcome"),
    meta: {
      layout: "default",
      title: "Welcome",
      requiresAuth: false,
    },
  },
  {
    path: "/overview",
    name: "Overview",
    component: () => import("@/views/Overview"),
    meta: {
      layout: "app",
      title: "Overview ",
      requiresAuth: true,
    },
  },
  {
    path: "/engagements",
    name: "Engagements",
    component: () => import("@/views/Engagements/Index"),
    meta: {
      layout: "app",
      title: "Engagements",
      requiresAuth: true,
    },
  },
  {
    path: "/engagements/add",
    name: "EngagementConfiguration",
    component: () => import("@/views/Engagements/Configuration/Index.vue"),
    meta: {
      layout: "app",
      title: "Add an Engagement",
      requiresAuth: true,
    },
  },
  {
    path: "/engagements/:id",
    name: "EngagementDashboard",
    component: () => import("@/views/Engagements/Dashboard"),
    meta: {
      layout: "app",
      title: "Engagement Dashboard",
      requiresAuth: true,
    },
  },
  {
    path: "/audiences",
    name: "Audiences",
    component: () => import("@/views/Audiences/Index"),
    meta: {
      layout: "app",
      title: "Audiences",
      requiresAuth: true,
    },
  },
  {
    path: "/audiences/add",
    name: "AudienceConfiguration",
    component: () => import("@/views/Audiences/Configuration.vue"),
    meta: {
      layout: "app",
      title: "Add an Audience",
      requiresAuth: true,
    },
  },
  {
    path: "/audiences/:id/insight",
    name: "AudienceInsight",
    component: () => import("@/views/Audiences/Insight.vue"),
    meta: {
      layout: "app",
      title: "Audience Insight",
      requiresAuth: true,
    },
  },
  {
    path: "/models",
    name: "Models",
    component: () => import("@/views/Models"),
    meta: {
      layout: "app",
      title: "Models",
      requiresAuth: true,
    },
  },
  {
    path: "/connections",
    name: "Connections",
    component: () => import("@/views/Connections/Index"),
    meta: {
      layout: "app",
      title: "Connections",
      requiresAuth: true,
    },
  },
  {
    path: "/datasources/add",
    name: "DataSourceConfiguration",
    component: () => import("@/views/Connections/Index"),
    meta: {
      layout: "app",
      title: "Add a Data Source",
      requiresAuth: true,
    },
  },
  {
    path: "/destinations/add",
    name: "DestinationConfiguration",
    component: () => import("@/views/Destinations/Configuration"),
    meta: {
      layout: "app",
      title: "Add a Destination",
      requiresAuth: true,
    },
  },
  {
    path: "/identity-resolution",
    name: "IdentityResolution",
    component: () => import("@/views/IdentityResolution/Index"),
    meta: {
      layout: "app",
      title: "Identity Resolution",
      requiresAuth: true,
    },
  },
  {
    path: "/customers",
    name: "CustomerProfiles",
    component: () => import("@/views/CustomerProfiles/Index"),
    meta: {
      layout: "app",
      title: "Customer Profiles",
      requiresAuth: true,
    },
  },
  {
    path: "/customers/:id",
    name: "CustomerProfileDetails",
    component: () =>
      import("@/views/CustomerProfiles/CustomerProfileDetails.vue"),
    meta: {
      layout: "app",
      title: "Customer Profile Details",
      requiresAuth: true,
    },
  },
  {
    path: "/notifications",
    name: "AlertsAndNotifications",
    component: () => import("@/views/AlertsAndNotifications/Index"),
    meta: {
      layout: "app",
      title: "Alerts and Notifications",
      requiresAuth: true,
    },
  },
  {
    path: "/settings",
    name: "Settings",
    component: () => import("@/views/Settings"),
    meta: {
      layout: "app",
      title: "Settings",
      requiresAuth: true,
    },
  },
  {
    path: "/login",
    name: "Login",
    component: () => import("@/views/Login"),
    meta: {
      layout: "default",
      title: "Login",
      requiresAuth: false,
    },
  },
  {
    path: "/login/callback",
    component: Auth.handleCallback(),
  },
  {
    path: "/components",
    name: "Components",
    component: () => import("@/components/common/Index"),
    meta: {
      layout: "default",
      title: "Common Components",
      requiresAuth: false,
    },
  },
]

routes.push(NotFoundRoute)

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes,
})

router.beforeEach(async (to, from, next) => {
  document.title = pageTitle(to.meta.title)

  const requiresAuth = to.matched.some((record) => record.meta.requiresAuth)

  if (requiresAuth && !(await Vue.prototype.$auth.isAuthenticated())) {
    next({
      path: "/login",
      query: { redirect: to.fullPath },
    })
  } else {
    next()
  }
})

export default router
