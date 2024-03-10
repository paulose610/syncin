import { createRouter, createWebHistory } from "vue-router";
import Home from "../views/Home.vue";
import Entry from "../views/Entry.vue";
import Userstore from "@/stores/User.js";
import { ref } from "vue"

const routes = [
  {
    path: "/",
    name: "home",
    component: Home,
    meta: { requiresAuth: true }
  },
  {
    path: "/entry",
    name: "entry",
    component: Entry,
  }, 
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});


router.beforeEach((to, from, next) => {
  if (to.meta.requiresAuth) {
    Userstore.dispatch('authenticate').then((authenticated) => {
      if (authenticated) {
        console.log('authenticated')
        next();
      } else {
        next({ name: 'entry' }); // Redirect to entry if not authenticated
      }
    });
  } else {
    next();
  }
});

export default router;
