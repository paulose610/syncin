<script setup>
import { onBeforeMount, ref, onMounted, computed } from "vue";
    import Libstore from "@/stores/Lib.js";
    import Userstore from "@/stores/User.js"
    
    const user=Userstore.getters.getuser();
    const usersongs = Libstore.getters.getsongs();
</script>
 
<template>
    <div class="d-flex">
    
    </div>   
</template>
 
<style scoped>

</style>