import Vue from "vue"
import VueRouter from "vue-router"

import Auth from "@okta/okta-vue"
import { pageTitle } from "@/utils"
import config from "@/config"

Vue.use(Auth, config.oidc)

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
    path: "/configuration",
    name: "Configuration",
    component: () => import("@/views/Settings"),
    meta: {
      layout: "app",
      title: "Configuration ",
      requiresAuth: true,
    },
  },
  //#region Data Management
  {
    path: "/datasources/:id",
    name: "DataSourceListing",
    component: () => import("@/views/DataSources/Listing.vue"),
    meta: {
      layout: "app",
      title: "Data source",
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
  //#endregion

  //#region Decisioning
  {
    path: "/models",
    name: "Models",
    component: () => import("@/views/Decisioning/Index"),
    meta: {
      layout: "app",
      title: "Models",
      requiresAuth: true,
    },
  },
  {
    path: "/models/:id/overview",
    name: "ModelDashboard",
    component: () => import("@/views/Decisioning/Dashboard"),
    meta: {
      layout: "app",
      title: "Models",
      requiresAuth: true,
    },
  },
  //#endregion

  //#region Customer Insights
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
  //#endregion

  //#region Orchestration
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
    path: "/audiences/:id/update",
    name: "AudienceUpdate",
    component: () => import("@/views/Audiences/Configuration.vue"),
    meta: {
      layout: "app",
      title: "Update an Audience",
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
    path: "/engagements/:id/update",
    name: "EngagementUpdate",
    component: () => import("@/views/Engagements/Configuration/Index.vue"),
    meta: {
      layout: "app",
      title: "Edit an Engagement",
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
    path: "/dataSources",
    name: "DataSources",
    component: () => import("@/views/Connections/Index"),
    meta: {
      layout: "app",
      title: "Data Sources",
      requiresAuth: true,
    },
  },

    {
    path: "/destinations",
    name: "Destinations",
    component: () => import("@/views/Connections/DestinationIndex"),
    meta: {
      layout: "app",
      title: "Destinations",
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

  // TODO: HUS-1253
  const isAuthenticated = await Vue.prototype.$auth.isAuthenticated()

  if (requiresAuth && !isAuthenticated) {
    sessionStorage.setItem("appRedirect", to.fullPath)
    next({
      path: "/login",
      query: { redirect: to.fullPath },
    })
  } else {
    next()
  }
})

export default router
