<template>
  <div class="root_page">
    <div class="header_box">
        <header_box></header_box>
    </div>
    <div class="content_box">
        <router-view></router-view>
    </div>
  </div>
</template>


<script setup>
import { ref } from 'vue'
import header_box from './headpage_file/header_box.vue';

</script>

<style scoped>
  
</style>