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

const requireAuth = (to, from, next) => {
  if (!auth.loggedIn()) {
    next({
      path: "/login",
      query: { redirect: to.fullPath },
    })
  } else {
    next()
  }
}

const routes = [
  {
    path: "/",
    name: "Welcome",
    component: Welcome,
    meta: {
      layout: "default",
      title: "Welcome | Hux Unified UI",
    },
  },
  {
    path: "/overview",
    name: "overview",
    beforeEnter: requireAuth,
    component: () => import("@/views/overview.vue"),
    meta: {
      layout: "app",
      title: "Overview  | Hux Unified UI",
    },
  },
  {
    path: "/campaign",
    name: "campaign",
    beforeEnter: requireAuth,
    component: () => import("@/views/campaign.vue"),
    meta: {
      layout: "app",
      title: "Campaign | Hux Unified UI",
    },
  },
  {
    path: "/audiences",
    name: "audiences",
    beforeEnter: requireAuth,
    component: () => import("@/views/audiences/index.vue"),
    meta: {
      layout: "app",
      title: "Audiences | Hux Unified UI",
    },
  },
  {
    path: "/models",
    name: "models",
    beforeEnter: requireAuth,
    component: () => import("@/views/models.vue"),
    meta: {
      layout: "app",
      title: "Models | Hux Unified UI",
    },
  },
  {
    path: "/connections",
    name: "connections",
    beforeEnter: requireAuth,
    component: () => import("@/views/connections.vue"),
    meta: {
      layout: "app",
      title: "Connections | Hux Unified UI",
    },
  },
  {
    path: "/indentity",
    name: "indentity",
    beforeEnter: requireAuth,
    component: () => import("@/views/indentity.vue"),
    meta: {
      layout: "app",
      title: "Indentity | Hux Unified UI",
    },
  },
  {
    path: "/profiles",
    name: "profiles",
    beforeEnter: requireAuth,
    component: () => import("@/views/profiles.vue"),
    meta: {
      layout: "app",
      title: "Profiles | Hux Unified UI",
    },
  },
  {
    path: "/settings",
    name: "settings",
    beforeEnter: requireAuth,
    component: () => import("@/views/settings.vue"),
    meta: {
      layout: "app",
      title: "Settings | Hux Unified UI",
    },
  },
  {
    path: "/login",
    name: "login",
    component: Login,
    meta: {
      layout: "default",
      title: "Login | Hux Unified UI",
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
    component: () => import("@/components/common/CommonComponent"),
    meta: {
      layout: "app",
      title: "components",
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
  next()
})

export default router
