<script setup>
// @ is an alias to /src
import navbar from "@/components/navbar.vue";

</script>

<template>
  <div class="home">
    <navbar />
    <p>wlecome to home page</p>
  </div>
</template>

<style scope>
  .home{
    outline: 1px solid red;
  }
</style>