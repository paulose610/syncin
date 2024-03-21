<script setup>
import Userstore from "@/stores/User.js";
import Libstore from "@/stores/Lib.js";

import navbar from "@/components/navbar.vue";
import player from "@/components/player.vue";
import pbar from "@/components/cprofile/pbar.vue";
import modal from "@/components/cprofile/modal.vue";

import { ref, onMounted, onBeforeMount, toRaw, watch } from 'vue'

const mounted=ref(false);
const user=ref('');
onBeforeMount( async () => {
  await Userstore.dispatch('getuserinfo');
  user.value = Userstore.getters.getuser();
  await Libstore.dispatch('libload',user.value);
  mounted.value=true;
});

let type=ref('');
let typeprop=ref('');
function modaltype(payload){
  type.value=payload;
}
watch(type,(nval)=>{
  typeprop.value=nval;
})

</script>

<template>
  <div v-if="mounted" class="profilepage">
    <navbar />
    <div class="profilecontent d-flex justify-content-between" style="width:100%;height: 79vh;">
      <div class="maincontent d-flex flex-column justify-content-start align-items-center">     
          kvgrhkgjhi
      </div>
      <div class="pbar d-flex">
      <pbar @modaltype="modaltype"/>
      </div>
    </div>
    <player class="fixed-bottom"/>
  </div>
  <modal v-if="mounted" :type="typeprop" :user="user"/>
</template>

<style scoped>
    .pbar{
        height: 100%;
        align-items: center;
        }
    .maincontent{
        height: 79vh;
        background-color: rgb(198, 218, 196);
        width: 100%;
    }    
    .become{
      margin-top: 10px;
    }
</style>