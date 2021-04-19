import Vue from "vue"
import VueRouter from "vue-router"
import Home from "@/views/Home.vue"
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
      title: "Home",
    },
  },
  {
    path: "/overview",
    name: "overview",
    component: () => import("@/views/overview.vue"),
    beforeEnter: requireAuth,
    meta: {
      layout: "app",
      title: "overview",
    },
  },
  {
    path: "/campaign",
    name: "campaign",
    component: () => import("@/views/campaign.vue"),
    beforeEnter: requireAuth,
    meta: {
      layout: "app",
      title: "campaign",
    },
  },
  {
    path: "/audiences",
    name: "audiences",
    component: () => import("@/views/audiences/index.vue"),
    beforeEnter: requireAuth,
    meta: {
      layout: "app",
      title: "audiences",
    },
  },
  {
    path: "/models",
    name: "models",
    component: () => import("@/views/models.vue"),
    beforeEnter: requireAuth,
    meta: {
      layout: "app",
      title: "models",
    },
  },
  {
    path: "/connections",
    name: "connections",
    component: () => import("@/views/connections.vue"),
    beforeEnter: requireAuth,
    meta: {
      layout: "app",
      title: "connections",
    },
  },
  {
    path: "/indentity",
    name: "indentity",
    component: () => import("@/views/indentity.vue"),
    beforeEnter: requireAuth,
    meta: {
      layout: "app",
      title: "indentity",
    },
  },
  {
    path: "/profiles",
    name: "profiles",
    component: () => import("@/views/profiles.vue"),
    beforeEnter: requireAuth,
    meta: {
      layout: "app",
      title: "profiles",
    },
  },
  {
    path: "/settings",
    name: "settings",
    component: () => import("@/views/settings.vue"),
    beforeEnter: requireAuth,
    meta: {
      layout: "app",
      title: "settings",
    },
  },
  {
    path: "/login",
    name: "login",
    component: Login,
    meta: {
      layout: "default",
      title: "Login",
    },
  },
  {
    path: "/logout",
    beforeEnter(to, from, next) {
      auth.logout()
      next("/")
    },
  },
  {
    path: "/home",
    name: "Home",
    component: Home,
    beforeEnter: requireAuth,
    meta: {
      layout: "app",
      title: "Overview | Hux Unified UI",
    },
  },
  {
    path: "/components",
    name: "components",
    component: () => import("@/components/common/CommonComponent"),
    beforeEnter: requireAuth,
    meta: {
      layout: "default",
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
