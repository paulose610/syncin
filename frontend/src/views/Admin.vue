<script setup>
import Userstore from "@/stores/User.js";
import Libstore from "@/stores/User.js";

import navbar from "@/components/navbar.vue";
import player from "@/components/player.vue";
import pbar from "@/components/cprofile/pbar.vue";

import { ref, onMounted, onBeforeMount } from 'vue'

const mounted=ref(false);
const user=ref('');
onBeforeMount( async () => {
  await Userstore.dispatch('getuserinfo');
  user.value = Userstore.getters.getuser();
  await Libstore.dispatch('libload',user.value);
  mounted.value=true;
});
</script>

<template>
  <div v-if="mounted" class="profilepage">
    <navbar />
    <div class="profilecontent d-flex justify-content-end" style="width:100%;height: 79vh;">
      <div class="pbar d-flex">
      <pbar />
      </div>
    </div>
    <player class="fixed-bottom"/>
  </div>
</template>

<style scoped>
    .pbar{
        height: 100%;
        align-items: center;
        }
</style>