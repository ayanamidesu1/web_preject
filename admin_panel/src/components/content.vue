<template>
  <div class="content">
    <sidebar></sidebar>
    <div class="main">
        <router-view></router-view>
    </div>
  </div>
</template>


<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { BaseApi } from '@/base_api';
import { useStore } from '@/model/store/store';
import sidebar from './model/sidebar.vue';

const router = useRouter();
const store = useStore();
const api = new BaseApi();

</script>

<style scoped>
.content{
    display: grid;
    width: 90%;
    margin: 10px auto;
    grid-template-columns: minmax(150px,200px) minmax(400px,1fr);
    gap:10px;
}
</style>