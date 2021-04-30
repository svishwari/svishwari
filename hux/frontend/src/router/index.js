import Vue from "vue"
import VueRouter from "vue-router"
import Welcome from "@/views/Welcome.vue"
import Login from "@/views/Login.vue"
import NotFound from "@/views/NotFound.vue"

// Authentication Plugin
import auth from "@/auth"
// import config from '@/config';

Vue.use(VueRouter)

const NotFoundRoute = {
  path: "*",
  component: NotFound,
  meta: {
    title: "OOPs",
    layout: "default",
  },
}

const routes = [
  {
    path: "/",
    name: "Welcome",
    component: Welcome,
    meta: {
      layout: "default",
      title: "Welcome | Hux Unified UI",
      requiresAuth: false,
    },
  },
  {
    path: "/overview",
    name: "overview",
    component: () => import("@/views/Overview.vue"),
    meta: {
      layout: "app",
      title: "Overview  | Hux Unified UI",
      requiresAuth: true,
    },
  },
  {
    path: "/engagements",
    name: "engagements",
    component: () => import("@/views/Engagements.vue"),
    meta: {
      layout: "app",
      title: "Engagements | Hux Unified UI",
      requiresAuth: true,
    },
  },
  {
    path: "/audiences",
    name: "audiences",
    component: () => import("@/views/Audiences/Index.vue"),
    meta: {
      layout: "app",
      title: "Audiences | Hux Unified UI",
      requiresAuth: true,
    },
  },
  {
    path: "/models",
    name: "models",
    component: () => import("@/views/Models.vue"),
    meta: {
      layout: "app",
      title: "Models | Hux Unified UI",
      requiresAuth: true,
    },
  },
  {
    path: "/connections",
    name: "connections",
    component: () => import("@/views/Connections.vue"),
    meta: {
      layout: "app",
      title: "Connections | Hux Unified UI",
      requiresAuth: true,
    },
  },
  {
    path: "/datasources",
    name: "datasources",
    component: () => import("@/views/Connections.vue"),
    meta: {
      layout: "app",
      title: "Data Sources | Hux Unified UI",
      requiresAuth: true,
    },
  },
  {
    path: "/destinations",
    name: "destinations",
    component: () => import("@/views/Connections.vue"),
    meta: {
      layout: "app",
      title: "Destinations | Hux Unified UI",
      requiresAuth: true,
    },
  },
  {
    path: "/identity",
    name: "identity",
    component: () => import("@/views/Identity.vue"),
    meta: {
      layout: "app",
      title: "Identity | Hux Unified UI",
      requiresAuth: true,
    },
  },
  {
    path: "/profiles",
    name: "profiles",
    component: () => import("@/views/Profiles.vue"),

    meta: {
      layout: "app",
      title: "Profiles | Hux Unified UI",
      requiresAuth: true,
    },
  },
  {
    path: "/settings",
    name: "settings",
    component: () => import("@/views/Settings.vue"),

    meta: {
      layout: "app",
      title: "Settings | Hux Unified UI",
      requiresAuth: true,
    },
  },
  {
    path: "/login",
    name: "login",
    component: Login,
    meta: {
      layout: "default",
      title: "Login | Hux Unified UI",
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
  document.title = to.meta.title
  const requiresAuth = to.matched.some((record) => record.meta.requiresAuth)
  // Check for protected route
  if (requiresAuth && !auth.loggedIn()) {
    next({
      path: "/login",
      query: { redirect: to.fullPath },
    })
  } else next()
})

export default router
