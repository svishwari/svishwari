import Vue from "vue"
import VueRouter from "vue-router"

import auth from "@/auth"
import { pageTitle } from "@/utils"

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
    name: "overview",
    component: () => import("@/views/Overview"),
    meta: {
      layout: "app",
      title: "Overview ",
      requiresAuth: true,
    },
  },
  {
    path: "/engagements",
    name: "engagements",
    component: () => import("@/views/Engagements"),
    meta: {
      layout: "app",
      title: "Engagements",
      requiresAuth: true,
    },
  },
  {
    path: "/audiences",
    name: "audiences",
    component: () => import("@/views/Audiences/Index"),
    meta: {
      layout: "app",
      title: "Audiences",
      requiresAuth: true,
    },
  },
  {
    path: "/audiences/new",
    name: "createAudience",
    component: () => import("@/views/Audiences/Configuration.vue"),
    meta: {
      layout: "app",
      title: "Audiences",
      requiresAuth: true,
    },
  },
  {
    path: "/audiences/insight",
    name: "audienceInsight",
    component: () => import("@/views/Audiences/Insight.vue"),
    meta: {
      layout: "app",
      title: "Audiences",
      requiresAuth: true,
    },
  },
  {
    path: "/models",
    name: "models",
    component: () => import("@/views/Models"),
    meta: {
      layout: "app",
      title: "Models",
      requiresAuth: true,
    },
  },
  {
    path: "/connections",
    name: "connections",
    component: () => import("@/views/Connections"),
    meta: {
      layout: "app",
      title: "Connections",
      requiresAuth: true,
    },
  },
  {
    path: "/datasources",
    name: "datasources",
    component: () => import("@/views/Connections"),
    meta: {
      layout: "app",
      title: "Data Sources",
      requiresAuth: true,
    },
  },
  {
    path: "/connections/destinations/new",
    name: "add-destination",
    component: () => import("@/views/Destinations/Configuration.vue"),
    meta: {
      layout: "app",
      title: "Add a Destination",
      requiresAuth: true,
    },
  },
  {
    path: "/connections/destinations",
    name: "destinations",
    component: () => import("@/views/Destinations/Listing.vue"),
    meta: {
      layout: "app",
      title: "Destinations",
      requiresAuth: true,
    },
  },
  {
    path: "/identity",
    name: "identity",
    component: () => import("@/views/Identity"),
    meta: {
      layout: "app",
      title: "Identity",
      requiresAuth: true,
    },
  },
  {
    path: "/profiles",
    name: "profiles",
    component: () => import("@/views/Profiles"),
    meta: {
      layout: "app",
      title: "Profiles",
      requiresAuth: true,
    },
  },
  {
    path: "/settings",
    name: "settings",
    component: () => import("@/views/Settings"),
    meta: {
      layout: "app",
      title: "Settings",
      requiresAuth: true,
    },
  },
  {
    path: "/login",
    name: "login",
    component: () => import("@/views/Login"),
    meta: {
      layout: "default",
      title: "Login",
      requiresAuth: false,
    },
  },
  {
    path: "/logout",
    beforeEnter(to, from, next) {
      auth.logout()
      next("/login")
    },
  },
  {
    path: "/components",
    name: "components",
    component: () => import("@/components/common/Index"),
    meta: {
      layout: "default",
      title: "components",
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

router.beforeEach((to, from, next) => {
  document.title = pageTitle(to.meta.title)

  const requiresAuth = to.matched.some((record) => record.meta.requiresAuth)

  if (requiresAuth && !auth.loggedIn()) {
    next({
      path: "/login",
      query: { redirect: to.fullPath },
    })
  } else {
    next()
  }
})

export default router
