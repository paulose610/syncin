import { createRouter, createWebHistory } from "vue-router";
import Home from "../views/Home.vue";
import Entry from "../views/Entry.vue";
import Cprofile from "../views/Cprofile.vue";
import Uprofile from "../views/Uprofile.vue";
import Admin from "../views/Admin.vue";
import Userstore from "@/stores/User.js";
import Libstore from "@/stores/Lib.js";

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
  {
    path: "/cprofile",
    name: "cprofile",
    component: Cprofile,
    meta: { requiresAuth: true }
  }, 
  {
    path: "/uprofile",
    name: "uprofile",
    component: Uprofile,
    meta: { requiresAuth: true }
  },
  {
    path: "/admin",
    name: "admin",
    component: Admin,
    meta: { requiresAuth: true }
  }
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});


router.beforeEach((to, from, next) => {
  if (to.meta.requiresAuth) {
    Userstore.dispatch('authenticate').then((authorised) => {
      if (authorised) {
        if (to.name==='home'){
          console.log('authenticated');
          next();
        }
        else if (to.name==='cprofile' && authorised==='creator'){
          console.log('authorised:'+authorised);
          next();
        }
        else if (to.name==='uprofile' && ['creator', 'user'].includes(authorised)){
          console.log(authorised);
          next();
        }
        else if (to.name==='admin' && authorised==='admin'){
          console.log(authorised);
          next();
        }
        else{
          console.log('not authorised');
          next({name:'home'});
        }
      } 
      else next({name:'entry'});
    });
  } else {
    next();
  }
});

export default router;
