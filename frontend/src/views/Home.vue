<script setup>
import navbar from "@/components/navbar.vue";
import rsbar from "@/components/rsbar.vue";
import lsbar from "@/components/lsbar.vue";
import player from "@/components/player.vue"
import topsongs from "@/components/homep/topsongs.vue";

import { ref, onMounted, computed, onBeforeMount, toRaw } from 'vue'

import Libstore from "@/stores/Lib.js"
import Userstore from "@/stores/User.js"

const user=ref('');
const mounted=ref(false);
onBeforeMount( async () => {
  await Userstore.dispatch('getuserinfo');
  user.value = Userstore.getters.getuser();
  await Libstore.dispatch('libload',user.value);
  mounted.value=true;
});
 
let ls=ref(true);
let rs=ref(true);
 
const barchng=(bar)=>{
  if (bar==='ls') ls.value=!ls.value;
  else rs.value=!rs.value;
}
const barchk=(bar)=>{
  if (bar==='rs') return rs.value;
  else return ls.value;
}
</script>

<template>
  <div v-if="mounted" class="homepage"> 
    <navbar/>
    <div class="homecontent d-flex justify-content-center" style="width:100%;">
      <div class="bars ltb d-flex">
      <lsbar v-if="barchk('ls')"/>
      <button class="lsbut btn" @click="barchng('ls')">
        <i v-if="!barchk('ls')" class="bi bi-chevron-bar-right"></i>
        <i v-if="barchk('ls')" class="bi bi-chevron-bar-left"></i>
      </button>
      </div>
      <div class="discont">
          {{user.username}}
          <topsongs />
      </div>
      <div class="bars rtb d-flex">
      <button class="rsbut btn" @click="barchng('rs')">
        <i v-if="!barchk('rs')" class="bi bi-chevron-bar-left"></i>
        <i v-if="barchk('rs')" class="bi bi-chevron-bar-right"></i>
      </button>
      <rsbar v-if="barchk('rs')"/>
      </div>
    </div>
    <player class="fixed-bottom"/>
  </div>
</template>

<style scoped>
  .homepage{
    height: 100vh;
  }
  .homecontent{
    background-color: rgb(198, 218, 196);
    align-items: center;
    height:79vh;
  }
  .rsbut,.lsbut{
    background-color:#f8f9fa;
    height: 60px;
    border-radius: 0px;
  }
  .lsbut{
    border-top-right-radius: 10px; 
    border-bottom-right-radius: 10px;
  }
  .rsbut{
    border-top-left-radius: 10px; 
    border-bottom-left-radius: 10px;
  }
  .bars{
    height: 100%;
    align-items: center;
  }
  .discont {
  overflow: auto; 
  outline: 1px solid red;
  height: 79vh;
  }
</style>