import Vue from "vue";
import VueRouter from "vue-router";
import Home from "@/views/Home.vue";
import Welcome from "@/views/Welcome.vue";
import Login from "@/views/Login.vue";
import NotFound from "@/views/NotFound.vue";

// Authentication Plugin
import auth from "@/views/auth/auth";
// import config from '@/config';

Vue.use(VueRouter);

const NotFoundRoute = {
  path: "*",
  component: NotFound,
  meta: {
    title: "OOPs",
    layout: "default",
  },
};

const requireAuth = (to, from, next) => {
  if (!auth.loggedIn()) {
    next({
      path: "/login",
      query: { redirect: to.fullPath },
    });
  } else {
    next();
  }
};

const routes = [
  {
    path: "/",
    name: "Welcome",
    component: Welcome,
    meta: {
      layout: "default",
      title: "Welcome to Hux",
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
      auth.logout();
      next("/");
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
];
routes.push(NotFoundRoute);

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes,
});

router.beforeEach((to, from, next) => {
  document.title = to.meta.title;
  next();
});

export default router;
