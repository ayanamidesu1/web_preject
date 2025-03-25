<template>
  <div class="header_box">
    <head_title></head_title>
  </div>
</template>

<script>
// eslint-disable-next-line no-unused-vars
import { ref, reactive, toRefs, watch, onMounted, onUnmounted } from 'vue';
import head_title from './file/head_title.vue';
export default {
  name: 'header_box',
  components:{head_title},
}
</script>

<script setup>
</script>

<style scoped>
  
</style>