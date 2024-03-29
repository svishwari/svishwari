import Vue from "vue"
import VueRouter from "vue-router"

import Auth from "@okta/okta-vue"
import { pageTitle } from "@/utils"
import config from "@/config"
import { getAccess } from "../utils"

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
    path: "/home",
    name: "Home",
    component: () => import("@/views/Home.vue"),
    meta: {
      layout: "app",
      title: "Home ",
      requiresAuth: true,
    },
  },
  {
    path: "/clients",
    name: "ClientPanel",
    component: () => import("@/views/ClientPanel.vue"),
    meta: {
      layout: "app",
      title: "Client Panel ",
      requiresAuth: true,
    },
  },
  {
    path: "/configuration",
    name: "Configuration",
    component: () => import("@/views/Configuration/index.vue"),
    meta: {
      layout: "app",
      title: "Configuration ",
      requiresAuth: true,
    },
  },
  {
    path: "/my-issues",
    name: "MyIssues",
    component: () => import("@/views/MyIssues.vue"),
    meta: {
      layout: "app",
      title: "My Issues",
      requiresAuth: true,
    },
  },
  //#region Data Management
  {
    path: "/data-sources/:id",
    name: "DataSourceListing",
    component: () => import("@/views/DataSources/Listing.vue"),
    meta: {
      layout: "app",
      title: "Data source",
      requiresAuth: true,
    },
  },
  {
    path: "/data-sources/:id/datafeeds/:name",
    name: "DataSourceFeedsListing",
    component: () => import("@/views/DataSources/DataFeedsListing.vue"),
    meta: {
      layout: "app",
      title: "Data source",
      requiresAuth: true,
    },
  },
  {
    path: "/identity-resolution",
    name: "Identity",
    component: () => import("@/views/IdentityResolution/Index"),
    meta: {
      layout: "app",
      title: "Identity Resolution",
      requiresAuth: true,
    },
  },
  //#endregion

  //#region Models
  {
    path: "/models",
    name: "Models",
    component: () => import("@/views/Models/Index"),
    meta: {
      layout: "app",
      title: "Models",
      requiresAuth: true,
    },
  },
  {
    path: "/models/:id/overview",
    name: "ModelDashboard",
    component: () => import("@/views/Models/Dashboard"),
    meta: {
      layout: "app",
      title: "Model Dashboard",
      requiresAuth: true,
    },
  },
  {
    path: "/models/:id/overview/:version",
    name: "ModelDashboardVersion",
    component: () => import("@/views/Models/Dashboard"),
    meta: {
      layout: "app",
      title: "Model Dashboard",
      requiresAuth: true,
    },
  },
  //#endregion

  //#region Customer Insights
  {
    path: "/customers",
    name: "Customers",
    component: () => import("@/views/CustomerProfiles/Index"),
    meta: {
      layout: "app",
      title: "All Customers",
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
    path: "/segment-playground",
    name: "SegmentPlayground",
    component: () => import("@/views/SegmentPlayground/Index.vue"),
    meta: {
      layout: "app",
      title: "Segment Playground",
      requiresAuth: true,
    },
  },
  //#endregion

  // #region HX Trust ID
  {
    path: "/hx-trustid",
    name: "HXTrustID",
    component: () => import("@/views/HXTrustId/Index"),
    meta: {
      layout: "app",
      title: "HX TrustID",
      requiresAuth: true,
    },
  },
  // #endregion

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
      access: {
        screen: "audience",
        action: "create",
      },
    },
  },
  {
    path: "/audiences/:id/update",
    name: "AudienceUpdate",
    component: () => import("@/views/SegmentPlayground/Index.vue"),
    meta: {
      layout: "app",
      title: "Update an Audience",
      requiresAuth: true,
      access: {
        screen: "audience",
        action: "update_one",
      },
    },
  },
  {
    path: "/audiences/:id/clone",
    name: "CloneAudience",
    component: () => import("@/views/SegmentPlayground/Index.vue"),
    meta: {
      layout: "app",
      title: "Clone an Audience",
      requiresAuth: true,
      access: {
        screen: "audience",
        action: "create",
      },
    },
  },
  {
    path: "/audiences/:id/insight2",
    name: "AudienceInsight2",
    component: () => import("@/views/Audiences/Insight.vue"),
    meta: {
      layout: "app",
      title: "Audience Insight",
      requiresAuth: true,
    },
  },
  {
    path: "/audiences/:id/insight",
    name: "AudienceInsight",
    component: () => import("@/views/Audiences/Dashboard/Insight2.vue"),
    meta: {
      layout: "app",
      title: "Audience Insight",
      requiresAuth: true,
    },
  },
  {
    path: "/lookalike-audiences/:id/add",
    name: "LookalikeAudiences",
    component: () => import("@/views/Audiences/Lookalike/CreateLookalike.vue"),
    meta: {
      layout: "app",
      title: "Add an lookalike Audience",
      requiresAuth: true,
      access: {
        screen: "audience",
        action: "create_lookalike",
      },
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
    component: () => import("@/views/Engagements/Configuration/AddIndex.vue"),
    meta: {
      layout: "app",
      title: "Add an Engagement",
      requiresAuth: true,
      access: {
        screen: "engagements",
        action: "create_one",
      },
    },
  },
  //TODO: HUS-1817 remove once step 3 is also done.
  {
    path: "/eng/add",
    name: "EngagementAdd",
    component: () => import("@/views/Engagements/Configuration/AddIndex.vue"),
    meta: {
      layout: "app",
      title: "Add an Engagement",
      requiresAuth: true,
      access: {
        screen: "engagements",
        action: "create_one",
      },
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
      access: {
        screen: "engagements",
        action: "update_one",
      },
    },
  },
  {
    path: "/engagements/:id",
    name: "EngagementDashboard",
    component: () => import("@/views/Engagements/Dashboard/Index.vue"),
    meta: {
      layout: "app",
      title: "Engagement Dashboard",
      requiresAuth: true,
    },
  },

  {
    path: "/data-sources",
    name: "DataSources",
    component: () => import("@/views/DataSources/Index"),
    meta: {
      layout: "app",
      title: "Data Sources",
      requiresAuth: true,
    },
  },

  {
    path: "/destinations",
    name: "Destinations",
    component: () => import("@/views/Destinations/Index"),
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
      access: {
        screen: "destinations",
        action: "create_one",
      },
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
    path: "/email-deliverability",
    name: "EmailDeliverability",
    component: () => import("@/views/Measurement/EmailDeliverability/Index"),
    meta: {
      layout: "app",
      title: "Email Deliverability",
      requiresAuth: true,
    },
  },
  {
    path: "/application/add",
    name: "AddApplication",
    component: () => import("@/views/Application/AddApplication"),
    meta: {
      layout: "app",
      title: "Add an Application",
      requiresAuth: true,
      access: {
        screen: "applications",
        action: "create_application",
      },
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
    path: "/service-error",
    name: "ServiceError",
    component: () => import("@/views/ServiceError"),
    meta: {
      layout: "default",
      title: "Service Error",
      requiresAuth: true,
    },
  },
  {
    path: "/no-access-no-login",
    name: "NoAccessUserNotLogin",
    component: () => import("@/views/NoAccessUserNotLogin"),
    meta: {
      layout: "default",
      title: "No Access",
      requiresAuth: false,
    },
  },
  {
    path: "/no-access-login",
    name: "NoAccessUserLogin",
    component: () => import("@/views/NoAccessUserLogin"),
    meta: {
      layout: "default",
      title: "No Access",
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

  // TODO: need to perform RCA for the actual problem
  // THIS IS A TEMPORARY FIX
  let app = document.getElementById("app")
  let menuNodes = []
  app.childNodes.forEach((each) => {
    if (each.getAttribute("class").includes("menuable__content__active")) {
      menuNodes.push(each)
    }
  })
  menuNodes.forEach((each) => {
    each.style.display = "none"
  })

  const requiresAuth = to.matched.some((record) => record.meta.requiresAuth)

  // TODO: HUS-1253
  const isAuthenticated = await Vue.prototype.$auth.isAuthenticated()

  if (
    !to.meta.access ||
    getAccess(to.meta.access.screen, to.meta.access.action)
  ) {
    if (requiresAuth && !isAuthenticated) {
      sessionStorage.setItem("appRedirect", to.fullPath)
      next({
        path: "/login",
        query: { redirect: to.fullPath },
      })
    } else {
      next()
    }
  } else {
    next({
      path: "/no-access-login",
    })
  }
})

export default router
