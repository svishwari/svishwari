import Vue from "vue";
import VueRouter from "vue-router";
import Home from "@/views/Home.vue";
import Welcome from "@/views/Welcome.vue";
import Login from "@/views/Login.vue";
import NotFound from "@/views/NotFound.vue";
// import config from '@/config';

Vue.use(VueRouter);

const NotFoundRoute = {
  path: "*",
  component: NotFound,
  meta: {
    title: "OOPs",
    layout: "none",
  },
};

const routes = [
  {
    path: "/",
    name: "Home",
    component: Home,
    meta: {
      layout: "app",
      title: "Home",
    }
  },
  {
    path: "/overview",
    name: "overview",
    component: () => import('@/views/overview.vue'),
    meta: {
      layout: "app",
      title: "overview",
    },
  },
  {
    path: "/campaign",
    name: "campaign",
    component: () => import('@/views/campaign.vue'),
    meta: {
      layout: "app",
      title: "campaign",
    },
  },
  {
    path: "/audiences",
    name: "audiences",
    component: () => import('@/views/audiences/index.vue'),
    meta: {
      layout: "app",
      title: "audiences",
    },
  },
  {
    path: "/models",
    name: "models",
    component: () => import('@/views/models.vue'),
    meta: {
      layout: "app",
      title: "models",
    },
  },
  {
    path: "/settings",
    name: "settings",
    component: () => import('@/views/settings.vue'),
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
      layout: "none",
      title: "Login",
    },
  },
  {
    path: "/welcome",
    name: "Welcome",
    component: Welcome,
    meta: {
      layout: "none",
      title: "Welcome",
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
