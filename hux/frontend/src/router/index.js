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
