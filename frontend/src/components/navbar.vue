<script setup>
    import { ref, onBeforeMount, onMounted, defineProps } from 'vue'
    import { RouterLink } from 'vue-router';
    import Userstore from "@/stores/User";

    const user=Userstore.getters.getuser();

    const logout=()=>{
        Userstore.dispatch('logout');
    }
</script>

<template>
  <nav class="navbar navbar-expand-md navbar-light bg-light">
    <div class="container-fluid">
      <a class="navbar-brand" href="#">SYNCIN</a>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarSupportedContent">
        <ul class="navbar-nav me-auto mb-2 mb-lg-0 d-flex justify-content-between w-100">
          <li class="nav-item">
            <RouterLink to="/" class="Home btn">Home
                <i class="bi bi-house-door-fill"></i>
            </RouterLink>
          </li>
          <li class="nav-item" style="min-width:40%;">
            <form class="d-flex">
              <input class="form-control me-2" type="search" placeholder="Search" aria-label="Search">
              <button class="btn btn-outline-success" type="submit"><i class="bi bi-search"></i></button>
            </form>
          </li>
          <li class="nav-item d-flex">
           <div  v-if="user.role==='creator'" class="dropdown"> 
           <button class="Profile btn dropdown-toggle" type="button" data-bs-toggle="dropdown" aria-expanded="false">Profile
            <i class="bi bi-person"></i>
           </button>
           <ul class="dropdown-menu">
            <li><router-link to="/uprofile" class="dropdown-item">User</router-link></li>
            <li><router-link to="/cprofile" class="dropdown-item">Creator</router-link></li>
           </ul>
           </div>
           <div v-else-if="user.role==='user'">
            <RouterLink to="/uprofile" class="Profile btn">Profile
                <i class="bi bi-person"></i>
            </RouterLink>
           </div>
           <div v-else>
            <RouterLink to="/admin" class="Profile btn">Dashboard
                <i class="bi bi-laptop"></i>
            </RouterLink>
           </div>
           <button class="Logout btn" @click="logout">Logout
           <i class="bi bi-box-arrow-right"></i>
           </button>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<style scoped>
   nav{min-height: 10.5vh;} 
</style>